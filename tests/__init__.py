#!/usr/bin/env python
# encoding: utf-8

from attest import Tests
from tests.test_cgit import cgit
from tests.test_gitweb import gitweb

tests = (
    cgit,
    gitweb,
)

all = Tests(tests)

if __name__ == '__main__':
    all.main()
