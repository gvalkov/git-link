#!/usr/bin/env python
# encoding: utf-8

''' github tests '''

from tests.util import *

from attest import Tests
from scripttest import TestFileEnvironment

repourl = 'git@github.com:gvalkov/rsstail.py.git'
co_dir = '%s/github' % test_repo_dir


response_map = {
    ('commit', 'a45ee2c27d2c8106c92fee0d909c31b3b0f67cd8'):
        'https://github.com/gvalkov/rsstail.py/commit/a45ee2c27d2c8106c92fee0d909c31b3b0f67cd8',

    ('branch', 'master'):
        'https://github.com/gvalkov/rsstail.py/tree/master',

    ('tag', 'v0.1.1'):
        'https://github.com/gvalkov/rsstail.py/tree/v0.1.1',

    ('path', 'setup.py'):
        'https://github.com/gvalkov/rsstail.py/tree/7e21d59d7695330174dbfaed2582aa9c6b5d23cc/setup.py',

    ('path01', 'tests/'):
        'https://github.com/gvalkov/rsstail.py/tree/7e21d59d7695330174dbfaed2582aa9c6b5d23cc/tests',

    ('blob', 'v0.1.1:setup.py'):
        'https://github.com/gvalkov/rsstail.py/tree/3f0a595895d9ed0932af7de7229cec00f4acda4e/setup.py'
}


github = Tests()
repo = False


@github.context
def setup():
    global repo
    if not repo:
        repo = Repo(repourl, co_dir)
        repo.clone()
        repo.config('link.browser', 'github')
        repo.config('link.url', 'https://github.com/gvalkov/rsstail.py')

    try:
        repo.chdir()
        yield repo
    finally:
        pass


env = TestFileEnvironment(test_output_dir, cwd=co_dir)
create_tests(github, env, response_map, validate_url_404)

if __name__ == '__main__':
    github.main()
