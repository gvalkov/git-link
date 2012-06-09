#!/usr/bin/env python
# encoding: utf-8

import os, sys

from shutil import rmtree
from tempfile import mkdtemp
from functools import partial
from subprocess import call, check_call
from os.path import dirname, abspath, join as pjoin, isdir

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

from pytest import raises, set_trace, mark
from gitlink.main import main


here = dirname(abspath(__file__))
test_output_dir = pjoin(here, 'test-output')
test_repo_dir = pjoin(here, 'test-repos')


class Repo(object):
    def __init__(self, remote, local=None):
        self.remote = remote
        self.local = local if local else mkdtemp()

    def clone(self, overwrite=False):
        if isdir(self.local):
            return

        cmd = ('git', 'clone', self.remote, self.local)
        os.makedirs(self.local)
        check_call(cmd)

    def init(self):
        cmd = ('git', 'init', self.local)
        check_call(cmd)

    def config(self, key, value):
        cmd = ('git', '--git-dir=%s/.git' % self.local, 'config', key, value)
        check_call(cmd)

    def rmtree(self):
        rmtree(self.local)

    def chdir(self):
        os.chdir(self.local)


def validate_url_404(url):
    res = call('curl -sI "%s" | grep -iq "404 Not found"' % url, shell=True)
    return bool(res)


def mk_gitlink(url, codir, browser, linkurl):
    codir = '%s/%s' % (test_repo_dir, codir)

    repo = Repo(url, codir)
    repo.clone()
    repo.config('link.browser', browser)
    repo.config('link.url', linkurl)

    def gitlink(args):
        os.chdir(codir)
        oldargs = sys.argv[:]
        out = StringIO()
        try:
            sys.argv = ['gitlink'] + args.split(' ')
            main(out)
        finally:
            sys.argv = oldargs

        return out.getvalue().rstrip('\n')

    return gitlink
