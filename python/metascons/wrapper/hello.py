#!/usr/bin/env python
'''
A wrapper package for the 'later' package
'''

import os
from metascons.wrapper import Wrapper

class Hello(Wrapper):
    '''
    Record non standard info for the "Hello" package
    '''

    def install_target(self):
        return os.path.join(self.destbindir(),'bin',self.name())

    def make_target(self):
        dbgopt = 'opt'
        if '-dbg' == self.env('PLATFORM')[-4:]:
            dbgopt = 'dbg'
        return os.path.join(self.sourcedir(),dbgopt,self.name())


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

wrapper = Hello()

    

