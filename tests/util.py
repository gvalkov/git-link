#!/usr/bin/env python
# encoding: utf-8

import os, sys

from shutil import rmtree
from tempfile import mkdtemp
from functools import partial
from subprocess import call, check_call, check_output
from os.path import dirname, abspath, join as pjoin, isdir


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


def create_tests(suite, env, response_map, link_verifier=None):
    def _create(challenge, response, method):
        @suite.test
        def anon(repo):
            cmd = 'git link %s' % challenge
            anon.__doc__ = '%s - %s' % (method, cmd)

            res = env.run(cmd, expect_stderr=True).stdout.rstrip('\n')

            assert res == response, res + ' == ' + response

            if callable(link_verifier):
                assert link_verifier(res), 'link not reachable'

    for challenge, response in response_map.items():
        method, challenge = challenge
        _create(challenge, response, method)
