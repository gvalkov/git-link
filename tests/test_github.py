#!/usr/bin/env python
# encoding: utf-8

from util import *

res = [
    # branch
    ('master',
     'https://github.com/gvalkov/rsstail.py/tree/master'),

    # commit
    ('a45ee2c27d2c8106c92fee0d909c31b3b0f67cd8',
     'https://github.com/gvalkov/rsstail.py/commit/a45ee2c27d2c8106c92fee0d909c31b3b0f67cd8'),

    # tag by name
    ('v0.1.1',
     'https://github.com/gvalkov/rsstail.py/tree/v0.1.1'),

    # tag by sha
    ('42c7a1094a5bfe9adec228d65681940f9e673f7d',
     'https://github.com/gvalkov/rsstail.py/tree/v0.1.1'),

    # file path (HEAD)
    ('.gitignore',
     'https://github.com/gvalkov/rsstail.py/tree/790cc8cde0ef6c06443ee14c11ff7b1c6d3f22f4/.gitignore'),

    # dir path (HEAD)
    ('tests/',
     'https://github.com/gvalkov/rsstail.py/tree/790cc8cde0ef6c06443ee14c11ff7b1c6d3f22f4/tests'),

    # blob with tag
    ('v0.1.1:setup.py',
     'https://github.com/gvalkov/rsstail.py/tree/3f0a595895d9ed0932af7de7229cec00f4acda4e/setup.py'),

    # blob with commit
    ('9407973:.gitignore',
     'https://github.com/gvalkov/rsstail.py/tree/9407973348bf2250981c00aa5258c23bb2b04cdf/.gitignore'),

    # raw blob with commit
    ('-r 9407973:.gitignore',
     'https://raw.github.com/gvalkov/rsstail.py/9407973348bf2250981c00aa5258c23bb2b04cdf/.gitignore'),

    # branch/tag -- file
    ('v0.1.0 -- tests',
     'https://github.com/gvalkov/rsstail.py/tree/8c30df6a69052e02b67201d77ba2513ec832b530/tests'),

    # branch/tag -- file (short)
    ('-s 7 v0.1.0 -- tests',
     'https://github.com/gvalkov/rsstail.py/tree/8c30df6/tests'),
]

@pytest.fixture
def gitlink(request):
    url = 'git@github.com:gvalkov/rsstail.py.git'
    linkurl = 'https://github.com/gvalkov/rsstail.py'
    return mk_gitlink(url, 'github', 'github', linkurl, '790cc8cde0ef6c06443ee14c11ff7b1c6d3f22f4')

@mark.parametrize(('cmdargs', 'expect'), res)
def test_github_auto(gitlink, cmdargs, expect):
    assert gitlink(cmdargs) == expect
    assert validate_url_404(expect)
