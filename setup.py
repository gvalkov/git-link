#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup
from os.path import dirname, join as pjoin
from gitlink.version import version

here = dirname(__file__)

tests_require = ('attest', 'scripttest', 'mechanize', 'BeautifulSoup')

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

    'keywords'             : 'git gitweb cgit subcommand',
    'classifiers'          : classifiers,

    'url'                  : 'https://github.com/gvalkov/gitlink',

    'packages'             : ('gitlink',),
    'entry_points'         : {
        'console_scripts'  : ['git-link = gitlink.main:main']
    },

    'tests_require'        : tests_require,
    'test_loader'          : 'attest:auto_reporter.test_loader',
    'test_suite'           : 'tests.all',
}


setup(**kw)
