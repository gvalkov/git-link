*git-link*
----------

*Git-link* is a git sub-command for getting a repo-browser link to a
git object. The motivation behind *git-link* is that it is often
faster to navigate to a git object or path on the command line than it
is to click your way to it through a web interface. An example using
*git-link*'s github sources:

.. code-block:: bash

   $ git config --add link.url https://github.com/gvalkov/git-link
   $ git config --add link.browser github

   $ git link HEAD~10
   https://github.com/gvalkov/git-link/commit/d0bca29bd7

   $ git link v0.2.0
   https://github.com/gvalkov/git-link/tree/v0.2.0

   $ git link v0.2.0 -- setup.py
   https://github.com/gvalkov/git-link/tree/af4ad8c89b/setup.py

*Git-link* can be used with : cgit_, gitweb_, github_, github-private_

Install
=======

If you are familiar with installing package from PyPi:

.. code-block:: bash

    $ pip install gitlink

Otherwise, simply put the following file in your ``$PATH`` and make it executable::

    https://raw.githubusercontent.com/gvalkov/git-link/master/git-link

Usage
=====

::

    Usage: git link [options] <commit|tree|blob|path|branch|tag|diff>

    Options:
      -h, --help            show this help message and exit
      -v, --version         show version and exit
      -c, --clipboard       copy link to clipboard (overwrites link.clipboard)
      -u, --url <url>       repo browser url (overwrites link.url)
      -b, --browser <type>  repo browser type (overwrites link.browser)
      -s, --short <num>     truncate hashes to length (overwrites link.short)
      -r, --raw             show raw blob if possible

    Repo browsers:
      github-private cgit gitweb github

    Configuration:
      git config --add link.url <repo browser base url>
      git config --add link.browser <repo browser>
      git config --add link.clipboard false|true

    Examples:
      git link HEAD~10         url of 10th commit before HEAD
      git link v0.1.0^{tree}   url of tree object at tag v0.1.0
      git link master:file     url of file in branch master
      git link path/file       url of path/file in current branch
      git link devel -- path   url of path in branch devel
      git link v0.1.0          url of tag v0.1.0

Setup
=====

*Git-link* needs to know the name and url of the repository browser
for every repository it is being run in. This can be set through
``git-config`` or on the command line for each invocation:

.. code-block:: bash

    $ git config --add link.url <repo browser url>
    $ git config --add link.browser <repo browser name>
    $ git config --add link.clipboard false|true  # optional
    $ git config --add link.short 7  # optional
    $ git link --browser <url> --name <name> --clipboard ...

License
=======

*Git-link* is released under the terms of the `Revised BSD License`_.


Links
=====

Development:
    https://github.com/gvalkov/git-link

Package:
    http://pypi.python.org/pypi/gitlink

.. _cgit:       http://hjemli.net/git/cgit/
.. _gitweb:     http://git.kernel.org/?p=git/git.git;a=tree;f=gitweb;hb=refs/heads/master
.. _github:     http://github.com/
.. _github-private: https://github.com/plans
.. _`Revised BSD License`: https://raw.github.com/gvalkov/git-link/master/LICENSE
