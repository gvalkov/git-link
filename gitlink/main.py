# encoding: utf-8

'''
Git sub-command for getting a repo browser link to a git object.
'''

from __future__ import print_function, absolute_import

from optparse import OptionParser, make_option as mkopt
from sys import argv, exit, stderr, stdout, version_info

from . repobrowsers import repobrowsers, LinkType as LT
from . import git, version, utils


#-----------------------------------------------------------------------------
# Option parsing
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

Repo browsers:
  %s

Configuration:
  git config --add link.url <repo browser base url>
  git config --add link.browser <repo browser>
  git config --add link.clipboard false|true

Examples:
  git link HEAD~10         url of 10th commit before HEAD
  git link v0.1.0^{tree}   url of tree object at tag v0.1.0
  git link master:file     url of file in branch master
  git link path/file       url of path/file in current branch
  git link devel -- path   url of path in branch devel
  git link v0.1.0          url of tag v0.1.0''' % ' '.join(repobrowsers)

def parseopt(args=argv[1:]):
    opts = (
        mkopt('-h', '--help',      action='store_true'),
        mkopt('-v', '--version',   action='store_true'),
        mkopt('-c', '--clipboard', action='store_true'),
        mkopt('-r', '--raw',       action='store_true'),
        mkopt('-u', '--url',       action='store'),
        mkopt('-b', '--browser',   action='store', choices=list(repobrowsers)),
        mkopt('-s', '--short',     action='store'),
        mkopt('-t', '--traceback', action='store_true'),
    )

    parser = OptionParser(usage=usage, option_list=opts, add_help_option=False)
    opts, args = parser.parse_args(args)
    return parser, opts, args

def readopts(cmdargs=argv[1:]):
    '''Read configuration from command line or git config.'''

    parser, opts, args = parseopt(cmdargs)

    if opts.version:
        vstr = 'git-link version %s' % version
        print(vstr, file=stderr)
        exit(0)

    if opts.help or not args:
        print(usage)
        exit(0)

    cfg = git.get_config('link')

    # command line options overrule git config options
    opts.url = opts.url or cfg.get('url')
    opts.browser = opts.browser or cfg.get('browser')
    opts.clipboard = opts.clipboard or cfg.get('clipboard')
    opts.short = opts.short or cfg.get('short')

    errors = []
    if not opts.url:
        msg = "repo browser url not - use 'git config link.url' or '-u, --url'"
        errors.append(msg)
    if not opts.browser:
        msg = "repo browser type not set - use 'git config link.browser' or '-b, --browser'"
        errors.append(msg)

    if opts.short:
        try:
            opts.short = int(opts.short)
        except ValueError:
            msg = "invalid integer value for option 'git config link.short' or '-s, --short': %s"
            errors.append(msg % opts.short)

    if errors:
        print('\n'.join(errors), file=stderr)
        exit(1)

    return opts, args


#-----------------------------------------------------------------------------
def expand_args(ish, path):
    '''Determine *ish type and prepare response dict.'''

    if ish and path:
        res = git.path(path, ish)
        if not res:
            raise Exception('invalid reference: %s -- %s' % (ish, path))
        return res

    ret, t = git.run('git cat-file -t %s' % ish)
    res = {}

    if t == 'commit' and ish != 'HEAD':
        try:
            res = git.branch(ish)
        except:
            res = git.commit(ish)

    elif t == 'commit': res = git.commit(ish)
    elif t == 'tree':   res = git.tree(ish)
    elif t == 'blob':   res = git.blob(ish)
    elif t == 'tag':    res = git.tag(ish)
    else:
        res = git.path(ish, 'HEAD')

    if not res:
        res = {'type': LT.unknown}

    return res


#-----------------------------------------------------------------------------
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

def main(cmdargs=argv[1:], out=stdout):
    opts, args = readopts(cmdargs)

    if len(args) == 2:
        ish, path = args
    else:
        ish, path = args[0], None

    try:
        # instantiate repository browser
        rb = repobrowsers[opts.browser](opts.url)
    except KeyError as e:
        msg = 'repository browser "%s" not supported'
        print(msg % opts.browser, file=stderr)
        exit(1)

    try:
        # determine *ish type and expand
        res = expand_args(ish, path)
        if opts.short:
            utils.shorten_hashes(res, opts.short)
        link = get_link(res, rb, ish, opts.raw)
    except Exception as e:
        if opts.traceback:
            raise
        print(str(e), stderr)
        exit(1)

    if link and opts.clipboard:
        try:
            utils.to_clipboard(link)
        except Exception as e:
            if opts.traceback:
                raise
            print(str(e), file=stderr)

    if link:
        print(link, file=out)
