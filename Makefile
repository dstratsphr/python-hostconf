#
#  Handy targets to make things work
#

all: dist

README.rst:
	pandoc --from=markdown --to=rst --output README.rst README.md

clean:
	@rm -rf build
	@rm -f *~ README.rst MANIFEST

distclean: clean
	@find . -type d -name __pycache__ | xargs /bin/rm -rf
	@rm -rf venv dist

venv:
	@rm -rf venv
	$(PYTHON) -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install twine

dist: README.rst
	venv/bin/python3 setup.py sdist

clean-venv:
	@find venv/lib/python3.?/site-packages/ -name '*hostconf*' | xargs /bin/rm -rf
