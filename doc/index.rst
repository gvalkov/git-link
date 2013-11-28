Introduction
------------

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

*Git-link* can build urls for the following repo-browser: cgit_,
gitweb_, github_, github-private_


Usage
-----

::

    $ git link -h
    Usage: git link [options] <commit|tree|blob|path|branch|tag|diff>

    Options:
      -h, --help            show this help message and exit
      -v, --version         show version and exit
      -c, --clipboard       copy link to clipboard (overwrites link.clipboard)
      -u, --url <url>       repo browser base url (overwrites link.url)
      -b, --browser <type>  repo browser type (overwrites link.browser)
      -s, --short <num>     truncate hashes to length (overwrites link.short)
      -r, --raw             show raw blob if possible

    Available repo browsers:
      cgit github-private github gitweb

    Configuration:
      git config --add link.url <repo browser url>
      git config --add link.browser <repo browser>
      git config --add link.clipboard false|true

    Examples:
      git link HEAD~10        -> url to 10th commit before HEAD
      git link v0.1.0^{tree}  -> url to tree object at tag v0.1.0
      git link master:file    -> url to file in branch master
      git link path/file      -> url to path/file in current branch
      git link devel -- path  -> url to path in branch devel
      git link v0.1.0         -> url to tag v0.1.0


Installing
----------

The latest stable version of *git-link* is available on pypi, while
the development version can be installed from github:

.. code-block:: bash

    $ pip install gitlink  # latest stable version
    $ pip install git+git://github.com/gvalkov/git-link.git  # latest development version

Alternatively, you can install it manually like any other Python package:

.. code-block:: bash

    $ git clone git@github.com:gvalkov/git-link.git
    $ cd git-link
    $ git reset --hard HEAD $versiontag
    $ python setup.py install


Setup
-----

*Git-link* needs to know the name and url of the repository browser
for every repository it is being run in. This can be set through
``git-config`` or on the command line for each invocation:

.. code-block:: bash

    $ git config --add link.url <repo browser url>
    $ git config --add link.browser <repo browser name>
    $ git config --add link.clipboard false|true  # optional
    $ git config --add link.short 7  # optional
    $ git link --browser <url> --name <name> --clipboard ...


Shell completion
----------------

*Git-link* comes with shell completion for bash and zsh.

    - **bash:** copy git-link.sh_ to ``/etc/bash_completion.d/``.
    - **zsh:**  copy git-link.zsh_ anywhere in ``$fpath``.

If *git-link* is being installed system-wide, it will attempt to place
these files in the right locations.


Development
-----------

See repobrowsers.py_ and test_cgit.py_ if you are interested in adding
a new repository browser. Running ``py.test tests/`` before
committing is generally a good idea.

Please make do without bringing in any external dependencies. As nice
as GitPython_ and libgit2 are, anything that this tool needs from git
can be queried using the command line.


License
-------

Git link is released under the terms of the `Revised BSD License`_.


.. _cgit:       http://hjemli.net/git/cgit/
.. _gitweb:     http://git.kernel.org/?p=git/git.git;a=tree;f=gitweb;hb=refs/heads/master
.. _github:     http://github.com/
.. _repo.or.cz: http://repo.or.cz/
.. _github-private:    https://github.com/plans
.. _repobrowsers.py:   https://github.com/gvalkov/git-link/blob/master/gitlink/repobrowsers.py
.. _test_cgit.py:      https://github.com/gvalkov/git-link/blob/master/tests/test_cgit.py
.. _`Revised BSD License`: https://raw.github.com/gvalkov/git-link/master/LICENSE
.. _git-link.zsh:      https://github.com/gvalkov/git-link/blob/master/etc/_git-link
.. _git-link.sh:       https://github.com/gvalkov/git-link/blob/master/etc/git-link.sh
.. _GitPython: https://pypi.python.org/pypi/GitPython/
.. _PyGit2: https://pypi.python.org/pypi/pygit2
