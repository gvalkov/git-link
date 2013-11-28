#!/usr/bin/env python
# encoding: utf-8

from sys import getdefaultencoding
from subprocess import Popen, PIPE
from os.path import relpath

from gitlink.repobrowsers import LinkType as LT


_run_encoding = getdefaultencoding()


def run(*args, **kw):
    p = Popen(stdout=PIPE, stderr=PIPE, shell=True, *args, **kw)
    out, err = p.communicate()
    ret = p.poll()

    if ret:
        cmd = kw.get('args')
        if cmd is None:
            cmd = args[0]
        #raise sub.CalledProcessError(ret, cmd, output=err)

    if out:
        out = out.decode(_run_encoding)  # :todo: not really sure about this
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

    if r:
        return {}

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


def revparse(ish):
    r, out = run('git rev-parse %s' % ish)
    return out.rstrip('\n')


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

    res = dict([i.split(' ', 1) for i in out if i])
    res['sha'] = revparse(commitish)  # :todo: why am I doing this!?

    return res


def cat_tag(tag):
    ''' tag name or sha => {
          'object' : sha of object pointed by tag,
          'type'   : type of object pointed by tag,
          'tag'    : name of tag (if tag was a sha),
          'sha'    : revparsed sha of tag,
          'tagger' : ...}
    '''

    r, out = run('git cat-file tag %s' % tag)
    out = out.splitlines()[:4]
    res = dict([i.split(' ', 1) for i in out if i])

    res['sha'] = revparse(tag)

    return res


def commit(arg):
    ''' HEAD~10 -> actual commit sha and tree sha'''
    res = cat_commit(arg)

    return {'type': LT.commit,
            'sha':  res['sha'],
            'tree_sha': res['tree']}


def tag(arg):
    ''' tag name or sha -> cat_tag() '''
    res = cat_tag(arg)
    res['type'] = LT.tag

    return res


def tree(arg):
    ''' HEAD~~^{tree} -> actual tree sha '''

    return {'type': LT.tree,
            'sha':  revparse(arg)}


def blob(arg):
    ''' HEAD~2:main.py -> tree + blob + path relative to git topdir '''

    res = {
        'type':       LT.blob,
        'tree_sha':   None,
        'commit_sha': None,
        'path':       None, }

    if ':' in arg:
        # the commitish may also be a tag
        commitish, path = arg.split(':', 1)

        r, t = run('git cat-file -t %s' % commitish)
        if t == 'tag':
            commitish = cat_tag(commitish)['object']

        commitd = cat_commit(commitish)

        sha, t, tree_sha = _path(path.split('/'), commitd['tree'])

        r, topdir = run('git rev-parse --show-toplevel')

        res['path']       = relpath(path, topdir)
        res['tree_sha']   = tree_sha
        res['sha']        = sha
        res['commit_sha'] = commitd['sha']
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


def path(arg, commitish='HEAD'):
    res = {}

    top_tree_sha = '%s^{tree}' % commitish

    r, topdir = run('git rev-parse --show-toplevel')
    path = relpath(arg, topdir)

    stt = _path(path.split('/'), top_tree_sha)

    if stt: sha, type, tree_sha = stt
    else: return {}

    if type == 'blob':   res['type'] = LT.blob
    elif type == 'tree': res['type'] = LT.path

    r, t = run('git cat-file -t %s' % commitish)
    if t == 'tag':
        commitish = cat_tag(commitish)['object']
    res['commit_sha'] = revparse(commitish)

    res['path'] = path
    res['sha'] = sha  # tree or blob sha
    res['tree_sha'] = revparse(tree_sha)  # tree sha if blob, None otherwise
    res['top_tree_sha'] = revparse(top_tree_sha)

    return res  # :bug:


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

    res = {'type': LT.branch,
           'sha':  sha,
           'ref':  ref,
           'shortref': shortref, }

    return res


def diff(arg):
    ''' :todo: '''
    pass
