#!/usr/bin/env python
# encoding: utf-8

from sys import stdout
from os import getuid
from os.path import dirname, isdir, join as pjoin

from distutils.command.build import build
from distutils.core import Command
from setuptools import setup

from gitlink.version import version


here = dirname(__file__)

classifiers = (
    'Environment :: Console',
    'Topic :: Utilities',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.0',
    'Programming Language :: Python :: 3.1',
    'Programming Language :: Python :: 3.2',
    'License :: OSI Approved :: BSD License',
    'Development Status :: 5 - Production/Stable',
    #'Development Status :: 6 - Mature',
    #'Development Status :: 7 - Inactive',
)

kw = {
    'name'             : 'gitlink',
    'version'          : version(),
    'description'      : 'Git sub-command for getting a repo browser link to a git object',
    'long_description' : open(pjoin(here, 'README.rst')).read(),
    'url'              : 'https://github.com/gvalkov/git-link',
    'author'           : 'Georgi Valkov',
    'author_email'     : 'georgi.t.valkov@gmail.com',
    'license'          : 'Revised BSD License',
    'keywords'         : 'git gitweb github cgit subcommand',
    'classifiers'      : classifiers,
    'packages'         : ['gitlink'],
    'entry_points'     : {'console_scripts': ['git-link = gitlink.main:main']},
    'data_files'       : [('share/man/man1', ['doc/git-link.1'])],
    'tests_require'    : ['pytest'],
    'cmdclass'         : {},
    'zip_safe'         : False,
}


class BuildDoc(Command):
    description = 'Generate man page'

    source = 'doc/git-link-man1.rst'
    dest = 'doc/git-link.1'

    user_options = []

    def initialize_options(self): pass
    def finalize_options(self): pass

    def run(self):
        from subprocess import check_call as c

        stdout.write('updating version: %s\n' % version())
        c('sed -i -e "s,\(:Version: *\).*,\\1%s," %s' % (version(), self.source), shell=True)

        stdout.write('generating man page: %s' % self.dest)
        c('rst2man %s > %s' % (self.source, self.dest), shell=True)


class PyTest(Command):
    user_options = []
    def initialize_options(self): pass
    def finalize_options(self):   pass
    def run(self):
        from subprocess import call
        errno = call(('py.test', 'tests'))
        raise SystemExit(errno)

kw['cmdclass']['test'] = PyTest
kw['cmdclass']['doc']  = BuildDoc


# try to install bash and zsh completions (emphasis on the *try*)
if getuid() == 0:
    if isdir('/etc/bash_completion.d'):
        t = ('/etc/bash_completion.d/', ['etc/git-link.sh'])
        kw['data_files'].append(t)

    # this is only valid for fedora and most debians
    dirs = ['/usr/share/zsh/functions/Completion/Unix/',
            '/usr/share/zsh/site-functions']

    for dir in dirs:
        if isdir(dir):
            t = (dir, ['etc/_git-link'])
            kw['data_files'].append(t)
            continue

if __name__ == '__main__':
    setup(**kw)
