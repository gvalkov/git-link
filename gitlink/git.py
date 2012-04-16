#!/usr/bin/env python
# encoding: utf-8

from subprocess import Popen, PIPE
from os.path import relpath, exists

from gitlink.repobrowsers import names, LinkType as LT


def run(*args, **kw):
    p = Popen(stdout=PIPE, stderr=PIPE, shell=True, *args, **kw)
    out, err = p.communicate()
    ret = p.poll()

    if ret:
        cmd = kw.get('args')
        if cmd is None: cmd = args[0]
        #raise sub.CalledProcessError(ret, cmd, output=err)

    if out:
        out = out.rstrip('\n')

    return ret, out


def get_config(section, strip_section=True):
    ''' Get a git config section as a dictionary

        [link]
            clipboard = true
            browser = cgit
            url = false

        => {'clipboard' : True, 'browser' : 'cgit', 'url' : False}
        => {'link.clipboard': True ...} if not strip_section
    '''

    r, out = run('git config --get-regexp "%s\\..*"' % section)

    if r: return {}

    def parse_helper(item):
        key, value = item

        if strip_section:
            key = key.replace(section+'.', '', 1)

        if value == 'true': value = True
        elif value == 'false': value = False

        return key, value

    out = out.splitlines()
    out = (i.split(' ', 1) for i in out)
    out = map(parse_helper, out)

    return dict(out)


def cat_commit(commitish):
    ''' commitish => {
          'commit'   : sha of commit pointed by commit-ish,
          'tree'     : ...,
          'parent'   : ...,
          'author'   : ...,
          'comitter' : ..., }
    '''

    r, out = run('git cat-file commit %s' % commitish)
    out = out.splitlines()[:4]
    res = dict([i.split(' ', 1) for i in out])

    r, out = run('git show -s --format="%%H" "%s"' % commitish)
    res['sha'] = out.splitlines()[-1]

    return res


def commit(arg):
    ''' HEAD~10 -> actual commit sha and tree sha'''
    res = cat_commit(arg)

    return { 'type' : LT.commit,
             'sha'  : res['sha'],
             'tree_sha' : res['tree'] }


def tree(arg):
    ''' HEAD~~^{tree} -> actual tree sha '''

    if '^{tree}' in arg:
        sha = arg.replace('^{tree}', '')
        sha = cat_commit(sha)['tree']
    else:
        sha = arg

    return { 'type' : LT.tree, 'sha' : sha }


def blob(arg):
    ''' HEAD~2:main.py -> tree + blob + path relative to git topdir '''

    res = {
        'type'       : LT.blob,
        'tree_sha'   : None,
        'commit_sha' : None,
        'path'       : None, }

    if ':' in arg:
        commitish, path = arg.split(':', 1)
        commitd = cat_commit(commitish)

        sha, t, tree_sha = _path(path.split('/'), commitd['tree'])

        r, topdir = run('git rev-parse --show-toplevel')

        res['path']       = relpath(path, topdir)
        res['commit_sha'] = commitd['sha']
        res['tree_sha']   = tree_sha
        res['sha']        = sha
    else:
        res['sha'] = arg

    return res


def lstree(sha):
    r, out = run('git ls-tree %s' % sha)

    for line in out.splitlines():
        mode, type, sha = line.split(' ', 3)
        sha, path = sha.split('\t', 1)

        yield mode, type, sha, path


def _path(arg, tree_sha='HEAD^{tree}'):
    ''' :param arg: a path.split('/') relative to root of the wc
        :param tree_sha: tree-ish to search

        if path leads to a  blob object return:
            blob sha, 'blob', tree sha
        if path leads to a tree object return:
            tree sha, 'tree', None
        if path does not exist, return None
    '''

    if not arg:
        return tree_sha, 'tree', None

    for m, t, sha, p in lstree(tree_sha):
        if p == arg[0] and t == 'tree':
            return _path(arg[1:], sha)

        if p == arg[0] and t == 'blob':
            return sha, 'blob', tree_sha


def path(arg, top_tree_sha='HEAD^{tree}'):
    res = {}

    r, topdir = run('git rev-parse --show-toplevel')
    path = relpath(arg, topdir)

    stt = _path(path.split('/'), top_tree_sha)

    if stt: sha, type, tree_sha = stt
    else:   return {}

    if type == 'blob'   : res['type'] = LT.blob
    elif type == 'tree' : res['type'] = LT.path

    res['path'] = path
    res['sha']  = sha # tree or blob sha
    res['tree_sha'] = tree_sha # tree sha if blob, None otherwise
    res['top_tree_sha'] = tree(top_tree_sha)['sha']
    res['commit_sha'] = cat_commit('HEAD')['sha']

    return res # :bug:


def branch(arg):
    ''' check if arg is a branch pointer '''

    remotes = run('git remote')[1].splitlines()

    r, sha = run('git show-ref "%s"' % arg)
    sha = sha.splitlines()[-1]
    sha, ref = sha.split(' ')

    shortref = None
    for i in remotes:
        if i in ref:
            shortref = ref.replace('refs/remotes/%s/' % i, '')
            break

    res = { 'type' : LT.branch,
            'sha'  : sha,
            'ref'  : ref,
            'shortref' : shortref, }

    return res


def diff(arg):
    ''' :todo: '''
    pass
