#!/usr/bin/env python
'''
A wrapper package for the 'later' package
'''

import os
from ext.wrapper import Wrapper

class Later(Wrapper):
    '''
    Record non standard info for the "Later" package
    '''

    def dependencies(self):
        'We need hello (no really, but pretend)'
        return ['hello']

    def tarball(self):
        return super(Later,self).tarball()[:-len('tar.gz')] + 'tgz'

    def install_target(self):
        return os.path.join(self.destbindir(),'bin',self.name())

    def make_target(self):
        return os.path.join(self.sourcedir(),self.name())


    def configure(self):
        self._env.Command(self.config_target(),self.unpack_target(),
                          'date > $TARGET')
        return

    def make(self):
        self._env.Command(self.make_target(),self.config_target(),
                          'cd %s ; scons' % self.sourcedir())
        return

    def install(self):
        self._env.Install(os.path.join(self.destbindir(),'bin'),
                          self.make_target())
        return


    pass

wrapper = Later()

    

