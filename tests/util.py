#!/usr/bin/env python
# encoding: utf-8

import pytest
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


run  = lambda *x,**kw: check_call(x, **kw)
here = dirname(abspath(__file__))
test_output_dir = pjoin(here, 'test-output')
test_repo_dir = pjoin(here, 'test-repos')


class Repo(object):
    def __init__(self, remote, local=None, headrev='HEAD'):
        self.remote = remote
        self.headrev = headrev
        self.local = local if local else mkdtemp()

    def clone(self, overwrite=False):
        if isdir(self.local):
            return
        os.makedirs(self.local)
        run('git', 'clone', self.remote, self.local)
        run('git', 'reset', '--hard', self.headrev, cwd=self.local)

    def init(self):
        run('git', 'init', self.local)

    def config(self, key, value):
        run('git', 'config', key, value, cwd=self.local)

    def rmtree(self):
        rmtree(self.local)

    def chdir(self):
        os.chdir(self.local)

def validate_url_404(url):
    res = call('curl -sI "%s" | grep -iq "404 Not found"' % url, shell=True)
    return bool(res)

def mk_gitlink(url, codir, browser, linkurl, headrev):
    codir = '%s/%s' % (test_repo_dir, codir)

    repo = Repo(url, codir, headrev)
    repo.clone()
    repo.config('link.browser', browser)
    repo.config('link.url', linkurl)

    def gitlink(args):
        os.chdir(codir)
        out = StringIO()
        main(args.split(' '), out)
        return out.getvalue().rstrip('\n')

    return gitlink
