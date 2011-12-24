#!/usr/bin/env python
'''
Handle installing and setting external packages
'''

import os

class Wrapper(object):
    '''
    Each external package should implement an instance of this class
    or a subclass and instantiate it as a top-level object called
    "wrapper".  The methods are to return information about the
    package.  
    '''

    def set_env(self,env):
        '''
        Set my env shortly after creation
        '''
        self._env = env
        return

    def env(self,var):
        return self._env.Dictionary()[var]

    def name(self):
        '''Return the canonical package name, by default return the
        class name lowercased'''
        return self.__class__.__name__.lower()

    def dependencies(self):
        '''Return a list of canonical package names of other packages
        that must be built before this on'''
        return []

    def version(self):
        '''Return the version string for the package, by default it is
        assumed to be held by the NAME_VERSION variable from the environment'''
        varname = self.name().upper() + '_VERSION'
        return self.env(varname)

    def sourcedir(self):
        '''
        Return the location of the unpacked source.  By default this
        is constructed from the BUILDAREA from the environment,
        package name and version.  It must match what the tarball
        unpacks to.
        '''
        builddir = self.env('BUILD_AREA')
        return os.path.join(builddir,self.name() + '-' + self.version())

    def tarball(self):
        '''
        Return the local filesystem location of the tarball holding
        the source.  By default this is constructed from the TARFILES
        env var and the name and version and .tgz.
        '''
        tarfiles = self.env('TAR_FILES')
        return os.path.join(tarfiles,self.name() + '-' + self.version() + '.tar.gz')

    def tarballurl(self):
        '''
        Return the URL to get the tarball.  By default this is built
        from WEBCACHEURL and tarball() filename
        '''
        tb = os.path.basename(self.tarball())
        wc = self.env('WEB_CACHE_URL')
        return os.path.join(wc,tb)
    
    def destbindir(self):
        '''
        Return the local filesystem directory where this package is
        installed.  By default it is constructed from
        INSTALL_AREA/NAME/VERSION/PLATFORM/
        '''
        return os.path.join(self.env('INSTALL_AREA'), self.name(),
                            self.version(), self.env('PLATFORM'))


    def unpack_target(self):
        return os.path.join(self.sourcedir(),self.name() + '.unpacked')

    def config_target(self):
        '''
        Return the config target file.  Default assumes autoconf is
        building the package and config.status indicates configuration
        is done.
        '''
        return os.path.join(self.sourcedir(),'config.status')

    def install_target(self):
        '''
        Return a file produced by the install.  Default assumes that
        the install() command produces a NAME.installed file.
        '''
        return os.path.join(self.destbindir(),self.name()+'.installed')

    def make_target(self):
        '''
        Return a file produced by a successful make.  Default assumes
        that the make() command produces a NAME.made file.
        '''
        return os.path.join(self.sourcedir(), self.name() + '.made')


    ## The remaining methods are for adding build commands ##

    def get(self):
        '''
        Default get method to download the source tarball
        '''
        # use wget - to do: check for wget to exist and try to fall
        # back to curl.
        self._env.Command(self.tarball(),'/dev/null',
                          "wget -O $TARGET %s" % self.tarballurl())
        return


    def unpack(self):
        '''
        Default unpack method
        '''
        tb = self.tarball()
        ext = os.path.splitext(tb)[1]
        if ".zip" == ext:
            self._env.Command(self.sourcedir(), self.tarball(),
                              "cd $BUILD_AREA ; unzip $SOURCE && touch %s" % self.unpack_target())
            return
        # assume it is a tar file
        tar = "tar -x"
        if ext in ['.gz','.tgz']:
            tar += " -z "
        elif ext in ['.bz2']:
            tar += " -j "
        tar += " -C %s -f %s " % (os.path.dirname(self.sourcedir()),
                                  self.tarball())
        tar += ' && touch %s' % self.unpack_target()
        print 'Setting up tar: %s' % tar
        self._env.Command(self.unpack_target(), self.tarball(), tar)
        return

    def configure(self):
        '''
        Default configure method assuming autoconf.
        '''
        cmd = 'cd %s; ./configure --prefix=%s' % \
            (self.sourcedir(), self.destbindir() )
        self._env.Command(self.config_target(), self.unpack_target(),cmd)
        return
                          

    def make(self):
        '''
        Default make method
        '''
        cmd = 'cd %s ; make && date > %s.made' % (self.sourcedir(), self.name())
        self._env.Command(self.make_target(),self.config_target(),cmd)
        return

    def install(self):
        '''
        Default install method
        '''  
        cmd = 'cd %s ; make install && date > %s' % \
            (self.sourcedir(), self.install_target())
        self._env.Command(self.install_target(),self.make_target(),cmd)
        return
    pass
