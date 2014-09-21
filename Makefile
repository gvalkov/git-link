EXCLUDE = \*__pycache__ \*.pyo \*.pyc \*__main__.py

git-link: git-link.zip
	echo "#!/usr/bin/env python" | cat - $< > $@
	chmod +x $@

git-link.zip:
	zip -0 -r $@ gitlink -x $(EXCLUDE)
	(cd gitlink && zip -0 ../$@ __main__.py)

clean:
	-rm git-link.zip git-link
