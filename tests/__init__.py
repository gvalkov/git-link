#!/usr/bin/env python
# encoding: utf-8

from attest import Tests
from tests.test_cgit import cgit

tests = (
    cgit,
)

all = Tests(tests)

if __name__ == '__main__':
    all.main()
