#!/usr/bin/env python
# encoding: utf-8

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
     'http://hjemli.net/git/cgit/tree/tests/setup.sh/?tree=138e4f6924ba176e05b95e9921bab419912b0e01'),

    # dir path (HEAD)
    ('tests/',
     'http://hjemli.net/git/cgit/tree/tests/?tree=138e4f6924ba176e05b95e9921bab419912b0e01'),

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

url = 'http://hjemli.net/git/cgit'
headrev = 'f9b801a1746d6c4476b230659d2e1f3714986550'

@pytest.fixture
def gitlink(request):
    return mk_gitlink(url, 'cgit', 'cgit', url, headrev)

@mark.parametrize(('cmdargs', 'expect'), res)
def test_cgit_auto_lib(gitlink, cmdargs, expect):
    assert gitlink[0](cmdargs)  == expect
    assert validate_url_404(expect)

@skipif_no_gitlink
@mark.parametrize(('cmdargs', 'expect'), res)
def test_cgit_auto_exe(gitlink, cmdargs, expect):
    assert gitlink[1](cmdargs)  == expect
    assert validate_url_404(expect)
