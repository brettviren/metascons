#!/usr/bin/env python
'''
A metascons wrapper module for the GNU hello package
'''

import os
from metascons.wrapper import MetaSconsWrapper

class HelloWrapper(MetaSconsWrapper):

    def tarballurl(self):
        urlpatt = 'http://ftp.gnu.org/gnu/hello/hello-%s.tar.gz'
        return urlpatt % self.env['HELLO_VERSION']


    def prepare_target(self):
        return os.path.join(self.sourcedir(), 'config.status')

    def prepare_action(self):
        return 'cd %s && ./configure' % self.sourcedir()

    def build_target(self):
        return os.path.join(self.sourcedir(), 'src/hello')

    def build_action(self):
        return "cd %s && make" % self.sourcedir()

    def install_target(self):
        return os.path.join(self.installdir(),'bin/hello')

    def install_action(self):
        return "cd $HELLO_SOURCEDIR && make prefix=$HELLO_INSTALLDIR install"
    pass

wrapper = HelloWrapper()



