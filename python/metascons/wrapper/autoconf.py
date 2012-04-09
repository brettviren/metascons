#!/usr/bin/env python
'''
Base class for autoconf built packages

This class extends the interface to allow subclasses to provide
*_options() methods for prepare, build and install
'''

import os
from metascons.wrapper import MetaSconsWrapper

class AutoconfWrapper(MetaSconsWrapper):

    # Extend MetaSconsWrapper interface

    def prepare_options(self):
        'Return any options to add to configure'
        return ""

    def build_options(self):
        'Return any options passed to make during build'
        return ""

    def install_options(self):
        'Return any options passed to "make install"'
        return "prefix=$%s_INSTALLDIR" % self.name().upper()

    # Override MetaSconsWrapper interface

    def prepare_target(self):
        return os.path.join(self.sourcedir(), 'config.status')

    def prepare_action(self):
        return 'cd %s && ./configure %s' % (self.sourcedir(), self.prepare_options())

    def build_target(self):
        return os.path.join(self.sourcedir(), 'src/%s'%self.name())

    def build_action(self):
        return "cd %s && make %s" % (self.sourcedir(), self.build_options())

    def install_target(self):
        return os.path.join(self.installdir(),'bin/%s' % self.name())

    def install_action(self):
        return "cd $%s_SOURCEDIR && make %s install" % \
            (self.name().upper(), self.install_options())

    pass


