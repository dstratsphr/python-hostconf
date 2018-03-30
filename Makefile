#
#  Handy targets to make things work
#

PYTHON?=/usr/bin/python3

all: dist

README:
	pandoc --from=markdown --to=rst --output README README.md

clean:
	@rm -rf build
	@rm -f *~ README MANIFEST

distclean: clean
	@find . -type d -name __pycache__ | xargs /bin/rm -rf
	@rm -rf venv dist

venv:
	@rm -rf venv
	$(PYTHON) -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install twine

dist: venv README
	venv/bin/python3 setup.py sdist

clean-venv:
	@find venv/lib/python3.?/site-packages/ -name '*hostconf*' | xargs /bin/rm -rf

upload: dist
	venv/bin/twine upload dist/hostconf*.tar.gz

test-upload: dist
	venv/bin/twine upload --repository-url https://test.pypi.org/legacy/ dist/hostconf*.tar.gz

#
#  PIP install from test-site:
#
#    pip install --index-url https://test.pypi.org/simple/ hostconf
#
