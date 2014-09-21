VERSION = $(shell grep -Eo '[0-9][0-9\.]+' gitlink/__init__.py)
EXCLUDE = \*__pycache__ \*.pyo \*.pyc \*__main__.py

git-link: git-link.zip
	echo "#!/usr/bin/env python" | cat - $< > $@
	chmod +x $@

git-link.zip:
	zip -0 -r $@ gitlink -x $(EXCLUDE)
	(cd gitlink && zip -0 ../$@ __main__.py)

doc/git-link.1: doc/git-link-man1.rst update-man-version
	rst2man $< > $@

test:
	py.test tests

clean:
	-rm git-link.zip git-link

update-man-version: doc/git-link-man1.rst
	sed -i -e "s,\(:Version: *\).*,\1$(VERSION)," $<

.PHONY: update-man-version test clean
