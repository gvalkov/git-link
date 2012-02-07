#!/usr/bin/env python
# encoding: utf-8

''' gitweb tests '''

from tests.util import *

from attest import Tests
from scripttest import TestFileEnvironment


gitweb = Tests()

url   = 'http://git.naquadah.org/git/oocairo.git'
codir = '%s/gitweb' % test_repo_dir
browserurl  = 'http://git.naquadah.org/?p=oocairo.git'
browsername = 'gitweb'


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


ctx = create_test_context(gitweb, url, codir, browsername, browserurl)
gitweb.context(ctx)

env = TestFileEnvironment(test_output_dir, cwd=codir)
create_tests(gitweb, env, response_map, validate_url_404)

if __name__ == '__main__':
    gitweb.main()

