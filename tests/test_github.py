#!/usr/bin/env python
# encoding: utf-8

''' github tests '''

from tests.util import *


res = [
    ('a45ee2c27d2c8106c92fee0d909c31b3b0f67cd8' , 'https://github.com/gvalkov/rsstail.py/commit/a45ee2c27d2c8106c92fee0d909c31b3b0f67cd8'),         #commit
    ('master'                                   , 'https://github.com/gvalkov/rsstail.py/tree/master'),                                          #branch
    ('v0.1.1'                                   , 'https://github.com/gvalkov/rsstail.py/tree/v0.1.1'),                                             #tag
    ('setup.py'                                 , 'https://github.com/gvalkov/rsstail.py/tree/7e21d59d7695330174dbfaed2582aa9c6b5d23cc/setup.py'),  #path
    ('tests/'                                   , 'https://github.com/gvalkov/rsstail.py/tree/7e21d59d7695330174dbfaed2582aa9c6b5d23cc/tests'),     #path01
    ('v0.1.1:setup.py'                          , 'https://github.com/gvalkov/rsstail.py/tree/3f0a595895d9ed0932af7de7229cec00f4acda4e/setup.py'),  #blob
]


def pytest_funcarg__gitlink(request):
    url = 'git@github.com:gvalkov/rsstail.py.git'
    linkurl = 'https://github.com/gvalkov/rsstail.py'
    return mk_gitlink(url, 'github', 'github', linkurl)


@mark.parametrize(('cmdargs', 'expect'), res)
def test_github_auto(gitlink, cmdargs, expect):
    assert gitlink(cmdargs) == expect

