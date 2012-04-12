#!/usr/bin/env python
# encoding: utf-8

''' cgit tests '''

from tests.util import *


res = [
    ('bebe89d7c11a92bf206bf6e528c51ffa8ecbc0d5' , 'http://hjemli.net/git/cgit/commit/?id=bebe89d7c11a92bf206bf6e528c51ffa8ecbc0d5'),                 # commit
    ('33e28db20cbae2aa513ccec38c7d4706654eed46' , 'http://hjemli.net/git/cgit/tree/?tree=33e28db20cbae2aa513ccec38c7d4706654eed46'),                 # tree
    ('origin/wip'                               , 'http://hjemli.net/git/cgit/log/?h=wip'),                                                          # branch
    ('v0.8.3'                                   , 'http://hjemli.net/git/cgit/tag/?id=v0.8.3'),                                                      # tag
    ('tests/setup.sh'                           , 'http://hjemli.net/git/cgit/tree/tests/setup.sh/?tree=2e1546b0557b7372764584ce19bd3f223eed09d8'),  # path
    ('tests/'                                   , 'http://hjemli.net/git/cgit/tree/tests/?tree=2e1546b0557b7372764584ce19bd3f223eed09d8'),           # path01
    ('v0.8.3~10:tests/setup.sh'                 , 'http://hjemli.net/git/cgit/tree/tests/setup.sh/?tree=97eff9d6f8333ab79b08a5af72b836736b10c280'),  # blob
]


def pytest_funcarg__gitlink(request):
    url = 'http://hjemli.net/git/cgit'
    return mk_gitlink(url, 'cgit', 'cgit', url)


@mark.parametrize(('cmdargs', 'expect'), res)
def test_cgit_auto(gitlink, cmdargs, expect):
    assert gitlink(cmdargs) == expect

