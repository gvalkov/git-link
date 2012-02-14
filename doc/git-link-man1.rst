========
git-link
========

---------------------------------------
get a repo browser link to a git object
---------------------------------------

:Author:    Georgi Valkov
:Copyright: New BSD License
:Version:   0.1.0
:Manual section: 1

SYNOPSIS
========

::

    git link [-hvcubr]  <commit>|<tree>|<path>|<tag>|<diff>
    git link [-r|--raw] <blob>
    git link [-b|--browser|-u|--url] <commit>|<tree>|<path>|<tag>|<diff>|<blob>


DESCRIPTION
===========

Git-link builds repository browser urls for git objects and paths in the
working copy. The motivation behind git-link is that it is often faster to
navigate to a git object or path on the command line than it is to click your
way to it through a web interface.


SETUP
=============

Git-link needs to know the name and url of the repository browser for every
repository it is being run in. They can be specified either through
git-config(1) or on the command line::

    git config --add link.url <repo browser url>
    git config --add link.browser <repo browser name>
    git config --add link.clipboard false|true
    git link   --browser <url> --name <name> --clipboard ...


EXAMPLES
========

**git link** HEAD~10       

    url to 10th commit before HEAD

**git link** v0.1.0^{tree}

    url to tree object at tag v0.1.0

**git link** --raw master:file

    url to raw file in branch master

**git link** path/file

    url to path/file in current branch

**git link** --clipboard v0.1.0 

    url to tag v0.1.0, copied to clipboard


OPTIONS
=======

-h,--help

    show help message and exit

-v,--version

    show version and exit

-c,--clipboard

    copy link to clipboard (overwrites git config link.clipboard)

-u,--url <url>

    repo browser base url (overwrites git config link.url)

-b,--browser <name>

    repo browser type (overwrites git config link.browser)

-r,--raw

    show raw blob if possible


NOTES
=====

The base repo browser url for gitweb must include the project name:

    **git config** --add  http://git.kernel.org/?p=git/git.git

It is not currently possible to specify the branch/tree that a path url should
refer to:

    **git link** master -- path/to/dir


SEE ALSO
========

``git-config(1)``, ``gitrevisions(7)``
