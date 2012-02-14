Git Link
========

Git link is a git sub-command for getting a repo-browser link to a git object.
The motivation behind git-link is that it is often faster to navigate to a git
object or path on the command line than it is to click your way to it through a
web interface.  

Git link can build urls for the following repo-browser:
cgit_, gitweb_, github_, github-private_


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
      -r, --raw             show raw blob if possible

    Available repo browsers:
      cgit github-private github gitweb

    Configuration:
      git config --add link.url <repo browser url>
      git config --add link.browser <repo browser>
      git config --add link.clipboard false|true

    Examples:
      git link HEAD~10       -> url to 10th commit before HEAD
      git link v0.1.0^{tree} -> url to tree object at tag v0.1.0
      git link master:file   -> url to file in branch master
      git link path/file     -> url to path/file in current branch
      git link v0.1.0        -> url to tag v0.1.0


Installing
----------

The latest stable version of git link is available on pypi, while the
development version can be installed from github::

    $ pip install gitlink  # latest stable version
    $ pip install git+git://github.com/gvalkov/git-link.git # latest development version

Alternatively, you can install it manually like any other python package:: 

    $ git clone git@github.com:gvalkov/git-link.git
    $ cd git-link
    $ git reset --hard HEAD $versiontag
    $ python setup.py install


Setup
-----

Git link needs to know the name and url of the repository browser for every
repository it is being run in. They can be specified either through git-config
or on the command line::

    $ git config --add link.url <repo browser url>
    $ git config --add link.browser <repo browser name>
    $ git config --add link.clipboard false|true # optional
    $ git link   --browser <url> --name <name> --clipboard ...


Shell completion
----------------

Git link comes with shell completion for bash and zsh.

    - **bash:** copy git-link.sh_ to ``/etc/bash_completion.d/`` (TBD)
    - **zsh:**  copy git-link.zsh_ anywhere in ``$fpath``

If you are installing system-wide, git link will attempt to place these files
in the right locations.


Development
-----------

See repobrowsers.py_ and test_cgit.py_ if you are interested in adding a new
repository browser.  Running ``python setup.py test`` or ``tests/__init__.py``
before committing is generally a good idea.

Please make do without bringing in any external dependencies. As nice as
GitPython and libgit2 are, anything that this tool needs from git can be
queried using the command line tools.


License
-------

Git link is released under the terms of the `New BSD License`_.


.. _cgit:       http://hjemli.net/git/cgit/
.. _gitweb:     http://git.kernel.org/?p=git/git.git;a=tree;f=gitweb;hb=refs/heads/master
.. _github:     http://github.com/
.. _repo.or.cz: http://repo.or.cz/
.. _github-private:    https://github.com/plans
.. _repobrowsers.py:   https://github.com/gvalkov/git-link/blob/master/gitlink/repobrowsers.py
.. _test_cgit.py:      https://github.com/gvalkov/git-link/blob/master/tests/test_cgit.py  
.. _`NEW BSD License`: https://raw.github.com/gvalkov/git-link/master/LICENSE
.. _git-link.zsh:      https://github.com/gvalkov/git-link/blob/master/etc/_git-link
.. _git-link.sh:       https://github.com/gvalkov/git-link/blob/master/etc/git-link.sh

