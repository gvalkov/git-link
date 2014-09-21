#!/usr/bin/env python
# encoding: utf-8

from util import *

res = [
    # commit
    ('90f02cb510335a5bfdb57f0c78915d5ac236013c',
     'http://git.naquadah.org/?p=oocairo.git;a=commitdiff;h=90f02cb510335a5bfdb57f0c78915d5ac236013c'),

    # tree
    ('90f02cb510335a5bfdb57f0c78915d5ac236013c^{tree}',
     'http://git.naquadah.org/?p=oocairo.git;a=tree;h=7d0f2011b9aa9343cf3ae6675416ddcbfddab7e9'),

    # branch
    ('master',
     'http://git.naquadah.org/?p=oocairo.git;a=shortlog;h=master'),

    # tag by name
    ('v1.4',
     'http://git.naquadah.org/?p=oocairo.git;a=commit;h=v1.4'),

    # tab by sha
    ('f8e35c47ddb48dfeffb1f80cf523ba3207b31aa1',
     'http://git.naquadah.org/?p=oocairo.git;a=commit;h=v1.3'),

    # file path (HEAD)
    ('test/context.lua',
     'http://git.naquadah.org/?p=oocairo.git;a=blob;h=472061f27b61d2bcba7a7dc75743a0e8db1a4e4c;f=test/context.lua'),

    # dir path (HEAD)
    ('test/',
     'http://git.naquadah.org/?p=oocairo.git;a=tree;f=test;h=8e941a88c606930750c98fc10927b17f0588cc8d'),

    # blob with tag
    ('v1.4:Changes',
     'http://git.naquadah.org/?p=oocairo.git;a=blob;h=5a2f18eac98afb6a601369f5fa867cd0d386b266;f=Changes'),

    # blob with commit
    ('47bf539:COPYRIGHT',
     'http://git.naquadah.org/?p=oocairo.git;a=blob;h=f90b1e3f8284f6a94f36919219acc575d9362e10;f=COPYRIGHT'),

    # raw blob with commit
    ('-r 47bf539:COPYRIGHT',
     'http://git.naquadah.org/?p=oocairo.git;a=blob_plain;h=f90b1e3f8284f6a94f36919219acc575d9362e10;f=COPYRIGHT'),

    # raw blob with commit (short)
    ('-s 7 -r 47bf539:COPYRIGHT',
     'http://git.naquadah.org/?p=oocairo.git;a=blob_plain;h=f90b1e3;f=COPYRIGHT'),
]

url = 'http://git.naquadah.org/git/oocairo.git'
linkurl = 'http://git.naquadah.org/?p=oocairo.git'
headrev = '2b40c79192e3c86074d21af51774971e19cbd2ab'

@pytest.fixture
def gitlink(request):
    return mk_gitlink(url, 'gitweb', 'gitweb', linkurl, headrev)

@mark.parametrize(('cmdargs', 'expect'), res)
def test_gitweb_auto_lib(gitlink, cmdargs, expect):
    assert gitlink[0](cmdargs)  == expect
    assert validate_url_404(expect)

@skipif_no_gitlink
@mark.parametrize(('cmdargs', 'expect'), res)
def test_gitweb_auto_exe(gitlink, cmdargs, expect):
    assert gitlink[1](cmdargs)  == expect
    assert validate_url_404(expect)
