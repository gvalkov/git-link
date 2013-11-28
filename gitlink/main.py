#!/usr/bin/env python
# encoding: utf-8

'''
Git sub-command for getting a repo browser link to a git object.
'''

import optparse

from sys import argv, exit, stderr, stdout, version_info

from gitlink.repobrowsers import names, LinkType as LT
from gitlink.version import version
from gitlink import git


basestr = (str, unicode) if version_info[0] == 2 else (str,)


# Configuring an optparse formatter is too verbose. This will do:
usage = '''\
Usage: git link [options] <commit|tree|blob|path|branch|tag|diff>

Options:
  -h, --help            show this help message and exit
  -v, --version         show version and exit
  -c, --clipboard       copy link to clipboard (overwrites link.clipboard)
  -u, --url <url>       repo browser url (overwrites link.url)
  -b, --browser <type>  repo browser type (overwrites link.browser)
  -s, --short <num>     truncate hashes to length (overwrites link.short)
  -r, --raw             show raw blob if possible

Available repo browsers:
  %s

Configuration:
  git config --add link.url <repo browser base url>
  git config --add link.browser <repo browser>
  git config --add link.clipboard false|true

Examples:
  git link HEAD~10        -> url to 10th commit before HEAD
  git link v0.1.0^{tree}  -> url to tree object at tag v0.1.0
  git link master:file    -> url to file in branch master
  git link path/file      -> url to path/file in current branch
  git link devel -- path  -> url to path in branch devel
  git link v0.1.0         -> url to tag v0.1.0
''' % ' '.join(names.keys())


def parseopt(args=None):
    o = optparse.make_option

    opts = (
        o('-h', '--help',      action='store_true'),
        o('-v', '--version',   action='store_true'),
        o('-c', '--clipboard', action='store_true'),
        o('-r', '--raw',       action='store_true'),
        o('-u', '--url',       action='store'),
        o('-b', '--browser',   action='store', choices=list(names.keys())),
        o('-s', '--short',     action='store', type='int'),
        o('-t', '--traceback', action='store_true'),
    )

    kw = {
        'usage': usage,
        'option_list': opts,
        'add_help_option': False,
    }

    p = optparse.OptionParser(**kw)
    #p.allow_interspersed_args = False

    if not args: o, a = p.parse_args()
    else:        o, a = p.parse_args(args)

    return p, o, a


def to_clipboard(s):
    '''Send string to clipboard.'''
    try:
        from gitlink.pyperclip import copy
    except:
        raise Exception('warning: xclip or xsel must be installed for copying to work')
    copy(s)


def readopts():
    '''Read configuration from command line or git config.'''

    parser, opts, args = parseopt()

    if opts.version:
        vstr = 'git-link version %s \n' % version()
        stderr.write(vstr)
        exit(0)

    if len(argv) == 1 or opts.help or not args:
        stderr.write(usage)
        exit(0)

    cfg = git.get_config('link')

    # command line > git config
    url = opts.url or cfg.get('url', None)
    browser = opts.browser or cfg.get('browser', None)
    clipboard = opts.clipboard or cfg.get('clipboard', None)
    short = opts.short or cfg.get('short', None)

    errors = []
    if not url:
        errors.append('repo browser url not set via "link.url" or "-u, --url"\n')
    if not browser:
        errors.append('repo browser type not set via "link.browser" or "-b, --browser"\n')

    if short:
        try: short = int(short)
        except ValueError:
            errors.append('invalid integer value for option "link.short": %s' % short)

    if errors:
        stderr.write(''.join(errors))
        exit(1)

    return url, browser, clipboard, short, args, opts.raw, opts


def expand_args(ish, path):
    '''Determine *ish type and prepare response dict.'''

    if ish and path:
        res = git.path(path, ish)
        if not res:
            raise Exception('invalid reference: %s -- %s' % (ish, path))
        return res

    r, t = git.run('git cat-file -t %s' % ish)

    res = {}

    if t == 'commit' and ish != 'HEAD':
        try:    res = git.branch(ish)
        except: res = git.commit(ish)

    elif t == 'commit': res = git.commit(ish)
    elif t == 'tree':   res = git.tree(ish)
    elif t == 'blob':   res = git.blob(ish)
    elif t == 'tag':    res = git.tag(ish)
    else:
        res = git.path(ish, 'HEAD')

    if not res:
        res = {'type': LT.unknown}

    return res


def get_link(r, rb, ish, raw=False):
    t = r['type']

    if t == LT.commit:
        link = rb.commit(r['sha'])

    elif t == LT.tree:
        link = rb.tree(r['sha'])

    elif t == LT.tag:
        link = rb.tag(r['tag'], r['sha'], r['object'])

    elif t == LT.branch:
        link = rb.branch(r['ref'], r['shortref'])

    elif t == LT.blob:
        link = rb.blob(r['sha'], r['path'], r['tree_sha'], r['commit_sha'], raw=raw)

    elif t == LT.path:
        link = rb.path(r['path'], r['sha'], r['commit_sha'])

    elif t == LT.unknown:
        raise Exception('unhandled object type')

    return link


def shorten_hashes(res, length=7):
    for key in 'sha', 'tree_sha', 'object', 'commit_sha', 'top_tree_sha':
        if key in res and isinstance(res[key], basestr):
            res[key] = res[key][:length]


def main(out=stdout):
    url, browser, clipboard, short, args, raw, opts = readopts()

    if len(args) == 2: ish, path = args
    else: ish, path = args[0], None

    # instantiate repository browser
    try:
        rb = names[browser](url)
    except KeyError as e:
        stderr.write('repository browser "%s" not supported\n' % browser)
        exit(1)

    # determine *ish type and expand
    try:
        res = expand_args(ish, path)
        if short: shorten_hashes(res, short)
        link = get_link(res, rb, ish, raw)
    except Exception as e:
        if opts.traceback:
            raise
        stderr.write(str(e) + '\n')
        exit(1)

    if link and clipboard:
        try:
            to_clipboard(link)
        except Exception as e:
            if opts.traceback: raise
            stderr.write(str(e)+'\n')

    if link:
        out.write(link+'\n')


if __name__ == '__main__':
    main()
