#!/usr/bin/env python
'''
Base class for autoconf built packages
'''

import os
from metascons.wrapper import MetaSconsWrapper

class AutoconfWrapper(MetaSconsWrapper):

    def prepare_target(self):
        return os.path.join(self.sourcedir(), 'config.status')

    def prepare_action(self):
        return 'cd %s && ./configure' % self.sourcedir()

    def build_target(self):
        return os.path.join(self.sourcedir(), 'src/%s'%self.name())

    def build_action(self):
        return "cd %s && make" % self.sourcedir()

    def install_target(self):
        return os.path.join(self.installdir(),'bin/%s' % self.name())

    def install_action(self):
        nam = self.name().upper()
        return "cd $%s_SOURCEDIR && make prefix=$%s_INSTALLDIR install"%(nam,nam)

    pass


