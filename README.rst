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


Documentation:
    http://git-link.readthedocs.org/en/latest/

Development:
    https://github.com/gvalkov/git-link

Package:
    http://pypi.python.org/pypi/gitlink
