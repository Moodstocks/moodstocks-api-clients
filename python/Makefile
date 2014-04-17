all:
	@echo "Nothing happens! Try 'make doc'."

.PHONY: doc
doc:
	mkdir -p doc/src
	cp moodstocks.py doc/src
	cp sphinx.conf.py doc/conf.py
	sphinx-apidoc --force --full -o doc doc/src >/dev/null
	cp sphinx.conf.py doc/conf.py
	pushd doc; \
	mv moodstocks.rst moodstocks.old; \
	sed '/undoc-members/d' moodstocks.old > moodstocks.rst; \
	sphinx-build -b html -d doctrees . html >/dev/null
	@echo
	@echo "Done. Open doc/html/moodstocks.html to browse documentation."

clean:
	rm -rf doc
