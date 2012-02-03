#!/usr/bin/env python
# encoding: utf-8

'''
Git subcommand for getting a repo browser link to a git object.
'''

import optparse
import textwrap
import subprocess as sub

from sys import argv, exit, stderr, stdout

from gitlink.repobrowsers import names
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


def main():
    url, browser, clipboard, args, raw = readopts()

    arg = args[0]
    res = expand_arg(arg)

    t = res['type']

    # instantiate repository browser
    rb = names[browser](url)

    if t == LT.commit:
        pass

    elif t == LT.tree:
        pass

    elif t == LT.tag:
        pass

    elif t == LT.branch:
        pass

    elif t in (LT.path, LT.blob):
        pass

    elif t == LT.unknown:
        exit(1)

    if link and clipboard:
        pass

    if link:
        stdout.write(link+'\n')


if __name__ == '__main__':
   main()
