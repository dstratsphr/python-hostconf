# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINX_APIDOC = sphinx-apidoc
SPHINXPROJ    = Python-Hostconf
SOURCEDIR     = source
BUILDDIR      = build
EXCLUDES      = ../hostconf/tests ../setup.py
TOPDIR        = ../

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

api-docs:
	@$(SPHINX_APIDOC) -o source $(TOPDIR) $(EXCLUDES) 

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
