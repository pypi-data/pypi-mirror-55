#!/usr/bin/env python
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
python-qpid-proton setup script

DISCLAIMER: This script took lots of inspirations from PyZMQ, which is licensed
under the 'MODIFIED BSD LICENSE'.

Although inspired by the work in PyZMQ, this script and the modules it depends
on were largely simplified to meet the requirements of the library.

The behavior of this script is to build the registered `_cproton` extension
using the installed Qpid Proton C library and header files. If the library and
headers are not installed, or the installed version does not match the version
of these python bindings, then the script will attempt to build the extension
using the Proton C sources included in the python source distribution package.

While the above removes the need of *always* having Qpid Proton C development
files installed, it does not solve the need of having `swig` and the libraries
qpid-proton requires installed to make this setup work.

From the Python side, this scripts overrides 1 command - build_ext - and it adds a
new one. The latter - Configure - is called from the former to setup/discover what's
in the system. The rest of the commands and steps are done normally without any kind
of monkey patching.
"""

import os
import shutil

import distutils.sysconfig as ds_sys
from distutils.ccompiler import new_compiler, get_default_compiler
from distutils.core import setup, Extension
from distutils.command.build import build
from distutils.command.build_ext import build_ext
from distutils.command.sdist import sdist
from distutils import errors

from setuputils import log
from setuputils import misc


_PROTON_VERSION=(0,
                 29,
                 0)
_PROTON_VERSION_STR = "%d.%d.%d" % _PROTON_VERSION


class CheckSDist(sdist):

    def run(self):
        self.distribution.run_command('configure')

        # Append the source that was removed during
        # the configuration step.
        _cproton = self.distribution.ext_modules[-1]
        _cproton.sources.append('cproton.i')

        try:
            sdist.run(self)
        finally:
            for src in ['cproton.py', 'cproton_wrap.c']:
                if os.path.exists(src):
                    os.remove(src)


class Configure(build_ext):
    description = "Discover Qpid Proton version"

    @property
    def compiler_type(self):
        compiler = self.compiler
        if compiler is None:
            return get_default_compiler()
        elif isinstance(compiler, str):
            return compiler
        else:
            return compiler.compiler_type

    def prepare_swig_wrap(self):
        """Run swig against the sources.  This will cause swig to compile the
        cproton.i file into a .c file called cproton_wrap.c, and create
        cproton.py.
        """
        ext = self.distribution.ext_modules[-1]

        if 'SWIG' in os.environ:
            self.swig = os.environ['SWIG']

        try:
            # This will actually call swig to generate the files
            # and list the sources.
            self.swig_sources(ext.sources, ext)
        except (errors.DistutilsExecError, errors.DistutilsPlatformError) as e:
            if not (os.path.exists('cproton_wrap.c') or
                    os.path.exists('cproton.py')):
                raise e

        # now remove the cproton.i file from the source list so we don't run
        # swig again.
        ext.sources = ext.sources[1:]
        ext.swig_opts = []

    def use_bundled_proton(self):
        """The proper version of libqpid-proton-core is not installed on the system,
        so use the included proton-c sources to build the extension
        """
        log.info("Building the bundled proton-c sources into the extension")

        setup_path = os.path.dirname(os.path.realpath(__file__))
        base = self.get_finalized_command('build').build_base
        build_include = os.path.join(base, 'include')
        proton_base = os.path.abspath(os.path.join(setup_path))
        proton_src = os.path.join(proton_base, 'src')
        proton_core_src = os.path.join(proton_base, 'src', 'core')
        proton_include = os.path.join(proton_base, 'include')

        log.debug("Using Proton C sources: %s" % proton_base)

        # Collect all the Proton C files packaged in the sdist and strip out
        # anything windows and configuration-dependent

        sources = []
        for root, _, files in os.walk(proton_core_src):
            for file_ in files:
                if file_.endswith(('.c', '.cpp')):
                    sources.append(os.path.join(root, file_))

        # Look for any optional libraries that proton needs, and adjust the
        # source list and compile flags as necessary.
        libraries = []
        includes = []
        macros = []

        # -D flags (None means no value, just define)
        macros += [('PROTON_DECLARE_STATIC', None)]

        if self.compiler_type=='msvc':
            sources.append(os.path.join(proton_src, 'compiler' , 'msvc', 'snprintf.c'))

        # Check whether openssl is installed by poking
        # pkg-config for a minimum version 0. If it's installed, it should
        # return True and we'll use it. Otherwise, we'll use the stub.
        if misc.pkg_config_version_installed('openssl', atleast='0'):
            libraries += ['ssl', 'crypto']
            includes += [misc.pkg_config_get_var('openssl', 'includedir')]
            sources.append(os.path.join(proton_src, 'ssl', 'openssl.c'))
        elif os.name=='nt':
            libraries += ['crypt32', 'secur32']
            sources.append(os.path.join(proton_src, 'ssl', 'schannel.c'))
        else:
            sources.append(os.path.join(proton_src, 'ssl', 'ssl_stub.c'))
            log.warn("OpenSSL not installed - disabling SSL support!")

        # create a temp compiler to check for optional compile-time features
        cc = new_compiler(compiler=self.compiler_type)
        cc.output_dir = self.build_temp

        # 0.10 added an implementation for cyrus. Check
        # if it is available before adding the implementation to the sources
        # list. 'sasl.c` and 'default_sasl.c' are added and one of the existing
        # implementations will be used.
        sources.append(os.path.join(proton_src, 'sasl', 'sasl.c'))
        sources.append(os.path.join(proton_src, 'sasl', 'default_sasl.c'))
        if cc.has_function('sasl_client_done', includes=['sasl/sasl.h'],
                           libraries=['sasl2']):
            libraries.append('sasl2')
            sources.append(os.path.join(proton_src, 'sasl', 'cyrus_sasl.c'))
        else:
            log.warn("Cyrus SASL not installed - only the ANONYMOUS and"
                     " PLAIN mechanisms will be supported!")
            sources.append(os.path.join(proton_src, 'sasl', 'cyrus_stub.c'))

        # Hack for Windows/msvc: We need to compile proton as C++, but it seems the only way to
        # force this in setup.py is to use a .cpp extension! So copy all the source files to .cpp
        # and use these as the compile sources
        if self.compiler_type=='msvc':
            targets = []
            target_base = os.path.join(self.build_temp, 'srcs')
            try:
                os.mkdir(target_base)
            except FileExistsError:
	            pass

            for f in sources:
                # We know each file ends in '.c' as we filtered on that above so just add 'pp' to end
                target = os.path.join(target_base, os.path.basename(f) + 'pp')
                shutil.copy(f, target)
                targets.append(target)

            # Copy .h files into temp tree too as we need them to compile
            for root, _, files in os.walk(proton_core_src):
                for file_ in files:
                    if file_.endswith('.h'):
                        shutil.copy(os.path.join(root, file_), os.path.join(target_base, file_))

            # Copy ssl/sasl .h files
            shutil.copy(os.path.join(proton_src, 'sasl', 'sasl-internal.h'), os.path.join(target_base, 'sasl-internal.h'))
            shutil.copy(os.path.join(proton_src, 'ssl', 'ssl-internal.h'), os.path.join(target_base, 'ssl-internal.h'))

            sources = targets

        # compile all the proton sources.  We'll add the resulting list of
        # objects to the _cproton extension as 'extra objects'.  We do this
        # instead of just lumping all the sources into the extension to prevent
        # any proton-specific compilation flags from affecting the compilation
        # of the generated swig code

        cc = new_compiler(compiler=self.compiler_type)
        ds_sys.customize_compiler(cc)

        extra = []
        if self.compiler_type=='unix':
            extra.append('-std=gnu99')
        objects = cc.compile(sources,
                             macros=macros,
                             include_dirs=[build_include,
                                           proton_include,
                                           proton_src]+includes,
                             # compiler command line options:
                             extra_preargs=extra,
                             output_dir=self.build_temp)

        #
        # Now update the _cproton extension instance passed to setup to include
        # the objects and libraries
        #
        _cproton = self.distribution.ext_modules[-1]
        _cproton.extra_objects = objects
        _cproton.include_dirs.append(build_include)
        _cproton.include_dirs.append(proton_include)

        # swig will need to access the proton headers:
        _cproton.swig_opts.append('-I%s' % build_include)
        _cproton.swig_opts.append('-I%s' % proton_include)

        # lastly replace the libqpid-proton-core dependency with libraries required
        # by the Proton objects:
        _cproton.libraries=libraries

    def libqpid_proton_installed(self, version):
        """Check to see if the proper version of the Proton development library
        and headers are already installed
        """
        return misc.pkg_config_version_installed('libqpid-proton-core', version)

    def use_installed_proton(self):
        """The Proton development headers and library are installed, update the
        _cproton extension to tell it where to find the library and headers.
        """
        # update the Extension instance passed to setup() to use the installed
        # headers and link library
        _cproton = self.distribution.ext_modules[-1]
        incs = misc.pkg_config_get_var('libqpid-proton-core', 'includedir')
        for i in incs.split():
            _cproton.swig_opts.append('-I%s' % i)
            _cproton.include_dirs.append(i)
        ldirs = misc.pkg_config_get_var('libqpid-proton-core', 'libdir')
        _cproton.library_dirs.extend(ldirs.split())

    def run(self):
        # check if the Proton library and headers are installed and are
        # compatible with this version of the binding.
        if self.libqpid_proton_installed(_PROTON_VERSION_STR):
            self.use_installed_proton()
        else:
            # Proton not installed or compatible, use bundled proton-c sources
            self.use_bundled_proton()
        self.prepare_swig_wrap()


class CustomBuildOrder(build):
    # The sole purpose of this class is to re-order
    # the commands execution so that `build_ext` is executed *before*
    # build_py. We need this to make sure `cproton.py` is generated
    # before the python modules are collected. Otherwise, it won't
    # be installed.
    sub_commands = [
        ('build_ext', build.has_ext_modules),
        ('build_py', build.has_pure_modules),
        ('build_clib', build.has_c_libraries),
        ('build_scripts', build.has_scripts),
    ]


class CheckingBuildExt(build_ext):
    """Subclass build_ext to build qpid-proton using `cmake`"""

    def run(self):
        # Discover qpid-proton in the system
        self.distribution.run_command('configure')
        build_ext.run(self)


# Override `build_ext` and add `configure`
cmdclass = {'configure': Configure,
            'build': CustomBuildOrder,
            'build_ext': CheckingBuildExt,
            'sdist': CheckSDist}

setup(name='python-qpid-proton',
      version=_PROTON_VERSION_STR + os.environ.get('PROTON_VERSION_SUFFIX', ''),
      description='An AMQP based messaging library.',
      author='Apache Qpid',
      author_email='users@qpid.apache.org',
      url='http://qpid.apache.org/proton/',
      packages=['proton'],
      py_modules=['cproton'],
      license="Apache Software License",
      classifiers=["License :: OSI Approved :: Apache Software License",
                   "Intended Audience :: Developers",
                   "Programming Language :: Python",
                   "Programming Language :: Python :: 2",
                   "Programming Language :: Python :: 2.6",
                   "Programming Language :: Python :: 2.7",
                   "Programming Language :: Python :: 3",
                   "Programming Language :: Python :: 3.3",
                   "Programming Language :: Python :: 3.4",
                   "Programming Language :: Python :: 3.5",
                   "Programming Language :: Python :: 3.6"],
      cmdclass=cmdclass,
      extras_require={
          'opentracing': ['opentracing', 'jaeger_client']
      },
      # Note well: the following extension instance is modified during the
      # installation!  If you make changes below, you may need to update the
      # Configure class above
      ext_modules=[Extension('_cproton',
                             sources=['cproton.i', 'cproton_wrap.c'],
                             swig_opts=['-threads'],
                             extra_compile_args=['-pthread'],
                             libraries=['qpid-proton-core'])])
