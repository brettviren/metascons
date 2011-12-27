#!/usr/bin/env python
'''
Base metascons build wrapper class
==================================

This module defines the base class MetaSconsWrapper.  It is meant to
illustrate the rules of metascons wrappers and provide default
behavior to other wrapper modules.  Actual modules should inherit from
this class and override methods in order to provide custom behavior.

Each module should store an instance in the top-level module variable
"wrapper":

::

  wrapper = MyMetaSconsWrapper()

The rest of this describes how metascons works and the rules that
wrapper classes should follow.

Build Stages
------------

A package build consists of a linear progression of different stages.
Each stage declares and produces an output "target" file that when
produced indicates the stage has been built (or rebuilt).  These
targets are then used for dependencies to trigger the next stage to
run.  If a stage needs not to perform any action it must still produce
a target file

The stages are:

download

  Download the source "tarball" (may be .zip or other collection of
  files).  The input target of this stage is /dev/null as scons does
  not handle a URL as a thing to calculate dependencies.  This stage
  must construct the URL from the environment.  The output target of
  this stage is a tarball file on the local filesystem.

unpack

  The tarball from the download stage is unpacked.  The output target
  should be some file indicating the unpacking succeeded.

prepare

  This stage prepares the unpacked source prior to building.  Its
  output target should be some file indicating the preparations are
  complete (even if none are needed).

build

  This stage performs any building of the package and provides a
  single file that indicates the build succeeded.

install

  This stage installs any results of the build into the install area.

Each stage has a ``STAGE_target`` and a ``STAGE_action`` method to
provide what is produced and how to produce it.  Details are below.

Describing things
-----------------

A stage's input and output targets and the command action needed to go
from one to the other can be specified in various levels of detail.
Some assumptions are made about common conventions and if the package
follows them its wrapper class can be brief.  If it deviates then
additional information needs to be provided. 

To describe how to fit the building of a package into metascons the
wrapper class overrides various methods in the MetaSconsWrapper class
below.

The information falls into these categories:

Inter-package Dependencies

  List of any packages that need to be built and installed before this
  one.

Build materials 

  Tarball url/files, source and install directories.

Intra-package Dependencies

  The representative "target" files that each stage produces.

Command Actions

  The command actions needed to carry the build from one stage to the
  next.  Details about actions follow.

Command Actions
---------------

Command actions implement what the stage does.  The term "action" is
follows the SCons definition.  They can be:

* Shell comand strings.

* Python functions with the signature ``action(target, source, env)``
  where target and source are lists (should be single-element here)
  and env is a SCons construction Environment.

* Instance of a SCons factory like Copy().

Actions should be written to remove its target file if it is
encountered and to not produce one unless the action succeeded.  

The default download and unpack actions should usually be sufficient
given the proper information is defined and likely do not need to be
defined by a wrapper.  On the other hand most wrappers will need to
define the prepare, build and install actions.

Target Files
------------

Target files indicate that a stage succeeded.  They are used by
metascons to assure dependecy order is correctly calculated.  They
provide a "big picture" of the build and are not typically "real"
files that participate in the actual detailed build.  The default
actions will produce a target file by storing the output of the
``date`` command into a text file named after the stage (as a
past-tense verb).  This will allow proper build and re-build ordering.

Environment
-----------

Every instance will be given a .env variable holding a SCons
Environment object and it will contain environment variables that
reference the build environment including what is needed to build/run
against other packages on which this one depends.

In addition, each class must implement an environment() method that
returns a dictionary containing environment variables to add to a more
full environment.  PATH-like values should stored as lists.

'''

import os

class MetaSconsWrapper(object):
    '''
    Baseclass for all metascons wrapper classes
    '''
    def set_env(self,env):
        'Set the ._env member, called by metascons'
        self.env = env
        return

    def name(self):
        'Canonical name - based on module name'
        name = self.__module__
        return name[name.rfind('.')+1:]


    ## Intra-package dependences ##

    def dependencies(self):
        '''
        Define a list of canonical package names (wrapper module names)
        that should be built before this package is built.  This function
        can be omitted if there are none.
        '''
        return []

    ## Build materials ##

    def version(self):
        '''
        Define the version string for the package as it will be used to
        identify source tarballs, source directories and create an
        installation area directory.  If omitted, the version will be
        taken from NAME_VERSION from the environment (ie, as set in the
        configuration file).
        '''
        return self.env[self.name().upper() + '_VERSION']

    def tarballname(self):
        '''
        Return the name (no path) of the tarball file holding the source.
        If omitted it is constructed from the name, version and .tar.gz
        extension.
        '''
        return self.name() + '-' + self.version() + '.tar.gz'

    def tarballurl(self):
        '''
        Define the URL from which to download the tarball.  If omiitted
        metascons assumes it is the WEB_CACHE_URL plus the tarballname
        '''
        return os.path.join(self.env['WEB_CACHE_URL'], self.tarballname())

    def tarballpath(self):
        '''
        Return the local filesyatem path to the tarball file holding the
        source.  If omitted it is constructed from the TAR_FILES and the
        tarballname
        '''
        return os.path.join(self.env['TAR_FILES'], self.tarballname())

    def sourcedir(self):
        '''
        Define the location of the unpacked source, that is, what
        unpacking the tarball produces.  If omitted it is constructed from
        the BUILD_AREA from the environment, package name and version.  It
        must match what the tarball unpacks to.
        '''
        return os.path.join(self.env['BUILD_AREA'], 
                            self.name() + '-' + self.version())

    def installdir(self):
        '''
        Define the local filesystem directory where this package is
        installed.  By default it is constructed from
        INSTALL_AREA/NAME/VERSION/PLATFORM/
        '''
        return os.path.join(self.env['INSTALL_AREA'], self.name(),
                            self.version(), self.env['PLATFORM'])

    def environment(self):
        '''
        Return a dictionary of environment variables needed to use the
        installed package.
        '''
        return {}


    ## targets: ##

    def download_target(self):
        '''
        Define a file that indicates the download it complete.  The
        default download action is such that the appearance of a file at
        tarballbath is suitable and this is the default.
        '''
        return self.tarballpath()

    def unpack_target(self):
        '''
        Define a file that is produced with the tarball is unpacked.  If
        omitted it will be set to SOURCEDIR/NAME.unpacked which is what
        the default unpacking command will produce.
        '''
        return os.path.join(self.sourcedir(),self.name() + '.unpacked')

    def prepare_target(self):
        '''
        Define the prepare target file.  If omitted it will be set to
        SOURCEDIR/NAME.prepared.  This is produced by the default prepare
        action.
        '''
        return os.path.join(self.sourcedir(),self.name() + '.prepared')

    def build_target(self):
        '''
        Define a file produced by a successful build of the code.  If
        omitted it will be SOURCEDIR/NAME.built.  This is produced by the
        default build action.
        '''
        return os.path.join(self.sourcedir(), self.name() + '.built')

    def install_target(self):
        '''
        Define a file produced by the install.  If omitted it will be set
        to INSTALLDIR/NAME.installed.
        '''
        return os.path.join(self.installdir(),self.name() + '.installed')

    def environment_target(self):
        '''
        Define a file produced during the environment generation
        stage.  If omitted it will be set to INSTALLDIR/setup-NAME.sh
        '''
        return os.path.join(self.installdir(),'setup-' + self.name() + '.sh')


    ## actions ##

    def download_action(self):
        '''
        Provide the action to download the tarball.  The default will
        download it based on tarballurl().  The download_target() is
        assumed to be the final resting spot for the tarball.
        '''
        import tempfile
        tdir = tempfile.mkdtemp()
        tfile = os.path.join(tdir,os.path.basename(self.tarballname()))

        return "cd $TAR_FILES && wget %s" % self.tarballurl()
         

    def unpack_action(self):
        '''
        Provide the action to unpack the tarball producing the sourcedir.
        The default handles .zip, .tar.gz, .tgz, .tar.bz2 and will unpack
        from the BUILD_AREA and assumes the result produces the expected
        sourcedir.  It produdes the output target as described above.
        '''

        tb = self.tarballname()
        ext = os.path.splitext(tb)[1]
        cmd = "rm -f %s ; cd $BUILD_AREA ; " % self.unpack_target()
        if ".zip" == ext:
            cmd += "unzip %s " % self.tarballpath()
        else:
            # assume it is a tar file
            tar = "tar -x"
            if ext in ['.gz','.tgz']:
                tar += " -z "
            elif ext in ['.bz2']:
                tar += " -j "
                pass
            tar += " -f %s " % self.tarballpath()
            cmd += tar
            pass
        cmd += " && date > %s" % self.unpack_target()
        return cmd

    def prepare_action(self):
        '''
        Provide a prepare action.  The default does nothing but produce
        the default prepare_target as described above.
        '''
        return "date > $TARGET"

    def build_action(self):
        '''
        Provide a build action.  The default does nothing but produce the
        build_target as described above.
        '''
        return "date > $TARGET"

    def install_action(self):
        '''
        Provide the install action.  The default does nothing but produce
        the install_target as described above.
        '''
        return "date > $TARGET"

    def do_environment_action(self,target,source,env):
        '''
        Generate setup scripts for this package.
        '''

        bs_name = self.environment_target()
        cs_name = os.path.splitext(bs_name)[0] + '.csh'

        bs_fp = open(bs_name,'w')
        cs_fp = open(cs_name,'w')

        head = '#!/bin/%s\n# generated setup script for %s.  Do not edit\n'
        bs_fp.write(head % ('sh',self.name()))
        cs_fp.write(head % ('csh',self.name()))

        for depobj in self.depobjs:
            other_bs_name = depobj.environment_target()
            other_cs_name = os.path.splitext(other_bs_name)[0] + '.csh'

            line = 'source %s\n'
            bs_fp.write(line % other_bs_name)
            cs_fp.write(line % other_cs_name)

            continue

        for key,val in self.environment().iteritems():
            if isinstance(val,list):
                val = ':'.join(val)
                # prepend to existing var
                bs_fp.write('export %s=%s${%s:+:$%s}\n' % (key,val,key,key))
                cs_fp.write('''
if ( $?%(key)s == 1 ) then
  setenv %(key)s %(val)s:${%(key)s}
else
  setenv %(key)s %(val)s
endif
''' % { 'key':key, 'val':val })
                continue
            bs_fp.write('export %s="%s"\n' % (key,val))
            cs_fp.write('setenv %s "%s"\n' % (key,val))
            continue

        return

    def environment_action(self):
        '''
        Provide the environment setup script generation action.  The
        default is to examine the INSTALLDIR.
        '''
        return self.do_environment_action


    pass
