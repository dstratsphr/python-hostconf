#!/usr/bin/python3
#
#  Tools for emulating a bit of autoconf/configure
#

import sys
import os
import sysconfig
import tempfile
import shutil

from pprint import PrettyPrinter

from distutils.errors import *
from distutils.ccompiler import new_compiler

pp = PrettyPrinter(indent=4)

class Configure(object):
    """Base class for common support aspects of the configuration process."""

    macros = []
    includes = []
    include_dirs = []
    libraries = []
    
    def __init__(self, verbose=0, dry_run=0, debug=False):
        self.compiler = new_compiler(verbose=verbose, dry_run=dry_run)
        #self.compiler.spawn = self.spawn
        self.debug = debug
        
        self.cache = {}
        self.config = {}

        self.tdir = tempfile.mkdtemp(prefix='hostconf_')
        print("TMPDIR:", self.tdir)
        self.conf_idx = 0

    def __del__(self):
        if not self.debug:
            shutil.rmtree(self.tdir)

    def spawn(self, cmd):
        print("spawn(): ", str(type(self)))
        print("spawn(): ", cmd)
        self.compiler.spawn(cmd)

    def _conftest_file(self,
                       pre_main=None, main=None,
                       header=None, includes=None, include_dirs=None):

        if includes is None:
            includes = []
        if include_dirs is None:
            include_dirs = []

        fname = 'conftest_{:03d}_'.format(self.conf_idx)
        self.conf_idx += 1

        # create the file
        fd,fname = tempfile.mkstemp('.c',
                                    prefix=fname, dir=self.tdir, text=True)

        # eventually, get the HAVE_* stuff
        conftext = []

        # setup the headers
        conftext += ['#include "%s"' % incl for incl in includes]

        # put the main header after the others
        if header is not None:
            conftext += ['#include "%s"' % header]

        # add in the precode
        if pre_main is not None:
            conftext += pre_main
            
        # setup the body
        conftext += ['int main(void) {']

        # add in the main code
        if main is not None:
            conftext += main

        # close the body
        conftext += [
            '    return 0;',
            '}'
        ]

        # create and fill the file
        with os.fdopen(fd, "w") as f:
            f.write(os.linesep.join(conftext))

        # just pass back the name
        return fd,fname

        
    def check_headers(self, headers, includes=None, include_dirs=None):
        results = []
        final_rv = False
        
        for header in headers:
            rv = self.check_header(header,
                                   includes=includes, include_dirs=include_dirs)
            results.append(rv)
            final_rv |= rv

        return final_rv, results
        
    def check_header(self, header, includes=None, include_dirs=None):

        # setup the message
        print('checking for {} ... '.format(header), end='')

        # create the conftest file
        fd,fname = self._conftest_file(header=header, includes=includes)

        # try to compile it 
        try:
            objects = self.compiler.compile([fname], include_dirs=include_dirs)
        except CompileError:
            print('no')
            return False

        tag = 'HAVE_' + header.replace('.', '_').upper()

        self.macros.append(tag)
        self.includes.append(header)
        self.config[tag] = 'yes'
        print('yes')
        return True

    def check_lib(self, funcname, library=None, includes=None, 
                  include_dirs=None, libraries=None, library_dirs=None):

        if includes is None:
            includes = []
        if include_dirs is None:
            include_dirs = []
        if libraries is None:
            libraries = []
        if library_dirs is None:
            library_dirs = []
        
        if library is None:
            libmsg = 'stdlibs'
            dashl = ''
        else:
            dashl = '-l' + library
            libraries.insert(0, library)
            libmsg = dashl
            
        print('checking for {} in {} ... '.format(funcname, libmsg), end='')

        # create the conftest file
        fd,fname = self._conftest_file(
            includes=includes,
            pre_main=['char {}();'.format(funcname)],
            main=['    {}();'.format(funcname),]
        )

        # eventually, get the HAVE_* stuff
        #conftext = []

        # setup the headers
        #conftext += ['#include "%s"' % incl for incl in includes]

        # setup the body
        #conftext += [
        #    'char {}();'.format(funcname),
        #    'int main(void) {',
        #    '    {}();'.format(funcname),
        #    '    return 0;',
        #    '}'
        #]

        # create and fill the file
        #fd, fname = self._conftest_file()
        #with os.fdopen(fd, "w") as f:
        #    f.write('\n'.join(conftext))

        # try to compile it 
        try:
            objects = self.compiler.compile([fname], include_dirs=include_dirs)
        except CompileError:
            print('no')
            return False

        # link it 
        try:
            self.compiler.link_executable(objects, "a.out",
                                 libraries=libraries,
                                 library_dirs=library_dirs)
        except (LinkError, TypeError):
            print('no')
            return False

        if library is not None:
            self.libraries.insert(0, library)
        
        print('yes')
        return True


    def check_decls(self):
        pass


if __name__ == '__main__':
    cf = Configure(debug=True)

    rv = cf.check_lib('el_init', 'edit')

    rv = cf.check_header('histedit.h')
    
    rv,l = cf.check_headers(['stdio.h', 'stdlib.h', 'string.h'])

    rv = cf.check_header('Python.h')

    print("LIBS:")
    pp.pprint(cf.libraries)
    print("Config:")
    pp.pprint(cf.config)
