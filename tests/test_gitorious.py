#!/usr/bin/env python
# encoding: utf-8

''' gitorious tests '''

from tests.util import *

from attest import Tests
from scripttest import TestFileEnvironment


gitorious = Tests()

url   = 'git://gitorious.org/maliit/maliit-framework.git'
codir = '%s/gitorious' % test_repo_dir
browserurl  = 'http://gitorious.org/maliit/maliit-framework'
browsername =  'gitorious'


response_map = {
    ('commit', '9cd9ebbd7948aa88dea2714d88d4a07833e77192'):
        'http://gitorious.org/maliit/maliit-framework/commit/9cd9ebbd7948aa88dea2714d88d4a07833e77192',

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


ctx = create_test_context(gitorious, url, codir, browsername, browserurl)
gitorious.context(ctx)

env = TestFileEnvironment(test_output_dir, cwd=codir)
create_tests(gitorious, env, response_map, validate_url_404)

if __name__ == '__main__':
    gitorious.main()
