#!/usr/bin/env python
# encoding: utf-8

from attest import Tests

from tests.test_cgit import cgit
from tests.test_gitweb import gitweb
from tests.test_github import github
from tests.test_gitorious import gitorious

tests = (
    cgit,
    gitweb,
    github,
    gitorious,
)

all = Tests(tests)

if __name__ == '__main__':
    all.main()
