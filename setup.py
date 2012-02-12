#!/usr/bin/env python
# encoding: utf-8

from os import getuid
from setuptools import setup
from os.path import dirname, isdir, join as pjoin
from gitlink.version import version

here = dirname(__file__)

tests_require = ('attest', 'scripttest')

classifiers = (
    'Environment :: Console',
    'Topic :: Utilities',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2.5',
    'License :: OSI Approved :: BSD License',
    #'Development Status :: 1 - Planning',
	'Development Status :: 2 - Pre-Alpha',
    # 'Development Status :: 3 - Alpha',
    #'Development Status :: 4 - Beta',
    #'Development Status :: 5 - Production/Stable',
    #'Development Status :: 6 - Mature',
    #'Development Status :: 7 - Inactive',
)

kw = {
    'name'                 : 'gitlink',
    'version'              : version(),

    'description'          : 'Git subcommand for getting a repo browser link to a git object',
    'long_description'     : open(pjoin(here, 'README.rst')).read(),

    'author'               : 'Georgi Valkov',
    'author_email'         : 'georgi.t.valkov@gmail.com',

    'license'              : 'New BSD License',

    'keywords'             : 'git gitweb github cgit subcommand',
    'classifiers'          : classifiers,

    'url'                  : 'https://github.com/gvalkov/git-link',

    'packages'             : ('gitlink',),
    'entry_points'         : {
        'console_scripts'  : ['git-link = gitlink.main:main']
    },

    'data_files'           : [('share/man/man1', ['doc/git-link.1'])],

    'tests_require'        : tests_require,
    'test_loader'          : 'attest:auto_reporter.test_loader',
    'test_suite'           : 'tests.all',

    'zip_safe'             : False,
}


from distutils.command.build import build
from distutils.core import Command

class BuildDoc(Command):
    description = 'Generate man page'

    source = 'doc/git-link-man1.rst'
    dest = 'doc/git-link.1'

    user_options = []

    def initialize_options(self): pass
    def finalize_options(self): pass

    def run(self):
        from subprocess import check_call as c

        print 'updating version: %s' % version()
        c('sed -i -e "s,\(:Version: *\).*,\\1%s," %s' % (version(), self.source), shell=True)

        print 'generating man page: %s' % self.dest
        c('rst2man %s > %s' % (self.source, self.dest), shell=True)


kw['cmdclass'] = {'doc' : BuildDoc}


# try to install bash and zsh completions (emphasis on the *try*)
if getuid() == 0:
    if isdir('/etc/bash_completion.d'):
        t = ('/etc/bash_completion.d/', ['etc/git-link.sh'])
        kw['data_files'].append(t)

    # this is only valid for most debians
    if isdir('/usr/share/zsh/functions/Completion/Unix/'):
        t = ('/usr/share/zsh/functions/Completion/Unix/', ['etc/_git-link'])
        kw['data_files'].append(t)


setup(**kw)
