#!/usr/bin/env python
# encoding: utf-8

''' cgit tests '''

from util import *


res = [
    # branch
    ('origin/wip',
     'http://hjemli.net/git/cgit/log/?h=wip'),

    # commit
    ('bebe89d7c11a92bf206bf6e528c51ffa8ecbc0d5',
     'http://hjemli.net/git/cgit/commit/?id=bebe89d7c11a92bf206bf6e528c51ffa8ecbc0d5'),

    # tree
    ('33e28db20cbae2aa513ccec38c7d4706654eed46',
     'http://hjemli.net/git/cgit/tree/?tree=33e28db20cbae2aa513ccec38c7d4706654eed46'),

    # tag by name
    ('v0.8.3',
     'http://hjemli.net/git/cgit/tag/?id=v0.8.3'),

    # tag by sha
    ('9094ee117ccbf5e76ec216548e2473aba70f1c8f',
     'http://hjemli.net/git/cgit/tag/?id=v0.8.3.2'),

    # file path (HEAD)
    ('tests/setup.sh',
     'http://hjemli.net/git/cgit/tree/tests/setup.sh/?tree=2e1546b0557b7372764584ce19bd3f223eed09d8'),

    # dir path (HEAD)
    ('tests/',
     'http://hjemli.net/git/cgit/tree/tests/?tree=2e1546b0557b7372764584ce19bd3f223eed09d8'),

    # blob with tag
    ('v0.8.3~10:tests/setup.sh',
     'http://hjemli.net/git/cgit/tree/tests/setup.sh/?tree=97eff9d6f8333ab79b08a5af72b836736b10c280'),

    # blob with commit
    ('7640d90:COPYING',
     'http://hjemli.net/git/cgit/tree/COPYING/?tree=a0ec3e5222dbb0cff965487def39f5781e5cb231'),

    # raw blob with commit
    ('-r 7640d90:COPYING',
     'http://hjemli.net/git/cgit/plain/COPYING/?tree=a0ec3e5222dbb0cff965487def39f5781e5cb231'),

    # raw blob with commit (short)
    ('-s 7 -r 7640d90:COPYING',
     'http://hjemli.net/git/cgit/plain/COPYING/?tree=a0ec3e5'),
]


def pytest_funcarg__gitlink(request):
    url = 'http://hjemli.net/git/cgit'
    return mk_gitlink(url, 'cgit', 'cgit', url)


@mark.parametrize(('cmdargs', 'expect'), res)
def test_cgit_auto(gitlink, cmdargs, expect):
    assert gitlink(cmdargs) == expect

