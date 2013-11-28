#!/usr/bin/env python
# encoding: utf-8

'''Version information constants and auxiliary functions.'''


VERSION = (0, 3, 0)

def version():
    return '.'.join([str(i) for i in VERSION])

__all__ = (VERSION, version)

if __name__ == '__main__':
    from sys import stdout
    v = 'git-link version %s' % version()
    stdout.write(v)
