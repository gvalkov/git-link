#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

from os import getuid
from os.path import isdir
from setuptools import setup

from gitlink import version


classifiers = [
    'Environment :: Console',
    'Topic :: Utilities',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'License :: OSI Approved :: BSD License',
    'Development Status :: 5 - Production/Stable',
]

kw = {
    'name':             'gitlink',
    'version':          version,
    'description':      'Git sub-command for getting a repo browser link to a git object',
    'long_description': open('README.rst').read(),
    'url':              'https://github.com/gvalkov/git-link',
    'author':           'Georgi Valkov',
    'author_email':     'georgi.t.valkov@gmail.com',
    'license':          'Revised BSD License',
    'keywords':         'git gitweb github cgit subcommand',
    'classifiers':      classifiers,
    'packages':         ['gitlink'],
    'entry_points':     {'console_scripts': ['git-link = gitlink.main:main']},
    'data_files':       [('share/man/man1', ['man/git-link.1'])],
    'tests_require':    ['pytest'],
    'zip_safe':         True,
}

# try to install bash and zsh completions (emphasis on the *try*)
if getuid() == 0:
    if isdir('/etc/bash_completion.d'):
        t = ('/etc/bash_completion.d/', ['etc/git-link.sh'])
        kw['data_files'].append(t)

    # this is only valid for fedora, freebsd and most debians
    dirs = ['/usr/share/zsh/functions/Completion/Unix/',
            '/usr/local/share/zsh/site-functions',
            '/usr/share/zsh/site-functions']

    for dir in dirs:
        if isdir(dir):
            t = (dir, ['etc/_git-link'])
            kw['data_files'].append(t)
            continue

if __name__ == '__main__':
    setup(**kw)
