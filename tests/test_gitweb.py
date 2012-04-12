#!/usr/bin/env python
# encoding: utf-8

''' gitweb tests '''

from tests.util import *


res = [
    ('90f02cb510335a5bfdb57f0c78915d5ac236013c'        , 'http://git.naquadah.org/?p=oocairo.git;a=commitdiff;h=90f02cb510335a5bfdb57f0c78915d5ac236013c'),                # commit
    ('90f02cb510335a5bfdb57f0c78915d5ac236013c^{tree}' , 'http://git.naquadah.org/?p=oocairo.git;a=tree;h=7d0f2011b9aa9343cf3ae6675416ddcbfddab7e9'),                      # tree
    ('master'                                          , 'http://git.naquadah.org/?p=oocairo.git;a=shortlog;h=master'),                                                    # branch
    ('v1.4'                                            , 'http://git.naquadah.org/?p=oocairo.git;a=commit;h=v1.4'),                                                        # tag
    ('test/context.lua'                                , 'http://git.naquadah.org/?p=oocairo.git;a=blob;h=472061f27b61d2bcba7a7dc75743a0e8db1a4e4c;f=test/context.lua'),   # path
    ('test/'                                           , 'http://git.naquadah.org/?p=oocairo.git;a=tree;f=test;h=e0032acb5f99f30f371d168bd8cae0597637b884'),               # path1
    ('v1.4:Changes'                                    , 'http://git.naquadah.org/?p=oocairo.git;a=blob;h=5a2f18eac98afb6a601369f5fa867cd0d386b266;f=Changes'),            # blob
]


def pytest_funcarg__gitlink(request):
    url = 'http://git.naquadah.org/git/oocairo.git'
    linkurl =  'http://git.naquadah.org/?p=oocairo.git'
    return mk_gitlink(url, 'gitweb', 'gitweb', linkurl)


@mark.parametrize(('cmdargs', 'expect'), res)
def test_gitweb_auto(gitlink, cmdargs, expect):
    assert gitlink(cmdargs) == expect

