#!/usr/bin/env python
# encoding: utf-8

''' gitweb tests '''

from tests.util import *

from attest import Tests
from scripttest import TestFileEnvironment

repourl = 'http://git.naquadah.org/git/oocairo.git'
co_dir = '%s/gitweb' % test_repo_dir


response_map = {
    ('commit', '90f02cb510335a5bfdb57f0c78915d5ac236013c'):
        'http://git.naquadah.org/?p=oocairo.git;a=commitdiff;h=90f02cb510335a5bfdb57f0c78915d5ac236013c',

    ('tree', '90f02cb510335a5bfdb57f0c78915d5ac236013c^{tree}'):
        'http://git.naquadah.org/?p=oocairo.git;a=tree;h=7d0f2011b9aa9343cf3ae6675416ddcbfddab7e9',

    ('branch', 'master'):
        'http://git.naquadah.org/?p=oocairo.git;a=shortlog;h=master',

    ('tag', 'v1.4'):
        'http://git.naquadah.org/?p=oocairo.git;a=commit;h=v1.4',

    ('path', 'test/context.lua'):
        'http://git.naquadah.org/?p=oocairo.git;a=blob;h=472061f27b61d2bcba7a7dc75743a0e8db1a4e4c;f=test/context.lua',

    ('path1', 'test/'):
        'http://git.naquadah.org/?p=oocairo.git;a=tree;f=test;h=e0032acb5f99f30f371d168bd8cae0597637b884',

    ('blob', 'v1.4:Changes'):
        'http://git.naquadah.org/?p=oocairo.git;a=blob;h=5a2f18eac98afb6a601369f5fa867cd0d386b266;f=Changes',
}


gitweb = Tests()
repo = False


@gitweb.context
def setup():
    global repo
    if not repo:
        repo = Repo(repourl, co_dir)
        repo.clone()
        repo.config('link.browser', 'gitweb')
        repo.config('link.url', 'http://git.naquadah.org/?p=oocairo.git')

    try:
        repo.chdir()
        yield repo
    finally:
        pass


env = TestFileEnvironment(test_output_dir, cwd=co_dir)
create_tests(gitweb, env, response_map)

if __name__ == '__main__':
    gitweb.main()

