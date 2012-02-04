#!/usr/bin/env python
# encoding: utf-8

'''
Git subcommand for getting a repo browser link to a git object.
'''

import optparse
import textwrap
import subprocess as sub

from sys import argv, exit, stderr, stdout
from os.path import relpath

from gitlink.repobrowsers import names, LinkType as LT
from gitlink.version import version_verbose


# Configuring an optparse formatter is too verbose. This will do:
usage = '''\
Usage: git link [options] <commit|tree|blob|path|branch|tag|diff>

Options:
  -h, --help            show this help message and exit
  -v, --version         show version and exit
  -c, --clipboard       copy link to clipboard (overwrites link.clipboard)
  -u, --url <url>       repo browser base url (overwrites link.url)
  -b, --browser <type>  repo browser type (overwrites link.browser)
  -r, --raw             show raw blob if possible

Available repo browsers:
  %s

Configuration:
  git config --add link.url <repo browser base url>
  git config --add link.browser <repo browser>
  git config --add link.clipboard false|true

Examples:
  git link HEAD~10       -> url to 10th commit prior to HEAD
  git link v0.1.0^{tree} -> url to tree object at tag v0.1.0
  git link master:file   -> url to file in branch master
  git link path/file     -> url to path/file in current branch
  git link v0.1.0        -> url to tag v0.1.0
''' % ' '.join(names.keys())


def parseopt(args=None):
    o = optparse.make_option

    opts = (
        o('-h', '--help',      action='store_true'),
        o('-v', '--version',   action='store_true'),
        o('-c', '--clipboard', action='store_true'),
        o('-r', '--raw',       action='store_true'),
        o('-u', '--url',       action='store'     ),
        o('-b', '--browser',   action='store', choices=names.keys()),
    )

    kw = {
        'usage'           : usage,
        'option_list'     : opts,
        'add_help_option' : False,
    }

    p = optparse.OptionParser(**kw)
    #p.allow_interspersed_args = False

    if not args: o, a = p.parse_args()
    else:        o, a = p.parse_args(args)

    return p, o, a


def run(*args, **kw):
    p = sub.Popen(stdout=sub.PIPE, stderr=sub.PIPE, shell=True, *args, **kw)
    out, err = p.communicate()
    ret = p.poll()

    if ret:
        cmd = kw.get('args')
        if cmd is None: cmd = args[0]
        #raise sub.CalledProcessError(ret, cmd, output=err)

    if out:
        out = out.rstrip('\n')

    return ret, out


def to_clipboard(s):
    ''' send string to clipboard '''
    try:
        from gitlink.pyperclip import copy
    except:
        raise Exception('warning: xclip must be installed for clipboard to work')

    copy(s)


def get_config(section, strip_section=True):
    ''' Get a git config section as a dictionary

        [link]
            clipboard = true
            browser = cgit
            url = false

        => {'clipboard' : True, 'browser' : 'cgit', 'url' : False}
        => {'link.clipboard': True ...} if not strip_section
    '''

    cmd = 'git config --get-regexp "%s\\..*"' % section

    p = sub.Popen(cmd, shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
    out, err = p.communicate()

    if p.poll():
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


def git_cat_commit(sha):
    ''' sha => {
          'tree'     : '',
          'parent'   : '',
          'author'   : '',
          'comitter' : '', }
    '''

    r, out = run('git cat-file commit %s' % sha)
    out = out.splitlines()[:4]

    res = dict([i.split(' ', 1) for i in out])
    return res


def readopts():
    ''' read configuration from command line or git config '''

    parser, opts, args = parseopt()

    if len(argv) == 1 or opts.help or not args:
        stderr.write(usage)
        exit(0)

    if opts.version:
        stderr.write(version_verbose() + '\n')
        exit(0)

    cfg = get_config('link')

    # command line > git config
    url = opts.url or cfg.get('url', None)
    browser = opts.browser or cfg.get('browser', None)
    clipboard = opts.clipboard or cfg.get('clipboard', None)

    errors = []
    if not url:
        errors.append('repo browser url not set via "link.url" or "-u, --url"\n')
    if not browser:
        errors.append('repo browser type not set via "link.browser" or "-b, --browser"\n')

    if errors:
        stderr.write(''.join(errors))
        exit(1)

    return url, browser, clipboard, args, opts.raw


def commit(arg):
    ''' HEAD~10 -> actual commit sha '''

    r, sha = run('git show -s --format=%%H "%s"' % arg)
    return { 'type' : LT.commit, 'sha' : sha }


def tree(arg):
    ''' HEAD~~^{tree} -> actual tree sha '''

    if '^{tree}' in arg:
        sha = arg.replace('^{tree}', '')
        sha = git_cat_commit(sha)['tree']
    else:
        sha = arg

    return { 'type' : LT.tree, 'sha' : sha }


def blob(arg):
    ''' HEAD~2:main.py -> tree hash + path relative to git topdir '''

    if ':' in arg:
        sym, path = arg.split(':', 1)

        r, sha = run('git log --all -n1 --format="%%T %%H" -- "%s" -- "%s"' % (sym, path))
        tree_sha, commit_sha = sha.split()

        r, topdir = run('git rev-parse --show-toplevel')

        res = { 'type' : LT.blob,
                'path' : relpath(path, topdir),
                'tree_sha'   : tree_sha,
                'commit_sha' : commit_sha, }

        return res


def path(arg):
    ''' main.py -> path relative to git topdir if path exists'''

    r, sha = run('git log --all -n1 --format="%%T %%H" -- "%s"' % arg)
    tree_sha, commit_sha = sha.split()

    if sha:
        r, topdir = run('git rev-parse --show-toplevel')

        res = { 'type' : LT.path,
                'path' : relpath(arg, topdir),
                'tree_sha'   : tree_sha,
                'commit_sha' : commit_sha, }

        return res


def branch(arg):
    ''' check if arg is a branch pointer '''

    r, sha = run('git show-ref "%s"' % arg)
    sha = sha.splitlines()[-1]
    sha, ref = sha.split(' ')

    res = { 'type' : LT.branch,
            'sha' : sha,
            'ref' : ref }

    return res


def diff(arg):
    pass


def expand_arg(arg):
    r, t = run('git cat-file -t %s' % arg)

    res = {}

    if t == 'commit' and arg != 'HEAD':
        try:
            res = branch(arg)
        except:
            res = commit(arg)

    elif t == 'commit':
        res = commit(arg)

    elif t == 'tree':
        res = tree(arg)

    elif t == 'blob':
        res = blob(arg)

    elif t == 'tag':
        res = { 'type' : LT.tag, 'sha' : None }

    # determine if arg is a path
    else:
        res = path(arg)

    if not res:
        res = {'type' : LT.unknown}

    return res


def main():
    url, browser, clipboard, args, raw = readopts()

    arg = args[0]
    res = expand_arg(arg)

    t = res['type']

    # instantiate repository browser
    rb = names[browser](url)

    if t == LT.commit:
        link = rb.commit(res['sha'])

    elif t == LT.tree:
        link = rb.tree(res['sha'])

    elif t == LT.tag:
        link = rb.tag(arg)

    elif t == LT.branch:
        link = rb.branch(res['ref'])

    elif t in (LT.path, LT.blob):
        link = rb.path(res['path'], res['tree_sha'], res['commit_sha'], raw=raw)

    elif t == LT.unknown:
        exit(1)

    if link and clipboard:
        try:
            to_clipboard(link)
        except Exception as e:
            stderr.write(str(e)+'\n')

    if link:
        stdout.write(link+'\n')


if __name__ == '__main__':
   main()
