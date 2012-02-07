#!/usr/bin/env python
# encoding: utf-8

''' cgit tests '''

from tests.util import *

from attest import Tests
from scripttest import TestFileEnvironment

repourl = 'http://hjemli.net/git/cgit'
co_dir = '%s/cgit' % test_repo_dir


response_map = {
    ('commit', 'bebe89d7c11a92bf206bf6e528c51ffa8ecbc0d5'):
        'http://hjemli.net/git/cgit/commit/?id=bebe89d7c11a92bf206bf6e528c51ffa8ecbc0d5',

    ('tree', '33e28db20cbae2aa513ccec38c7d4706654eed46'):
        'http://hjemli.net/git/cgit/tree/?tree=33e28db20cbae2aa513ccec38c7d4706654eed46',

    ('branch', 'origin/wip'):
        'http://hjemli.net/git/cgit/log/?h=wip',

    ('tag', 'v0.8.3'):
        'http://hjemli.net/git/cgit/tag/?id=v0.8.3',

    ('path', 'tests/setup.sh'):
        'http://hjemli.net/git/cgit/tree/tests/setup.sh/?tree=2e1546b0557b7372764584ce19bd3f223eed09d8',

    ('path01', 'tests/'):
        'http://hjemli.net/git/cgit/tree/tests/?tree=2e1546b0557b7372764584ce19bd3f223eed09d8',

    ('blob', 'v0.8.3~10:tests/setup.sh'):
        'http://hjemli.net/git/cgit/tree/tests/setup.sh/?tree=97eff9d6f8333ab79b08a5af72b836736b10c280'
}


cgit = Tests()
repo = False


@cgit.context
def setup():
    global repo
    if not repo:
        repo = Repo(repourl, co_dir)
        repo.clone()
        repo.config('link.browser', 'cgit')
        repo.config('link.url', repourl)

    try:
        repo.chdir()
        yield repo
    finally:
        pass


env = TestFileEnvironment(test_output_dir, cwd=co_dir)
create_tests(cgit, env, response_map, validate_url_404)

if __name__ == '__main__':
    cgit.main()
