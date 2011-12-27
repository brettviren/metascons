#!/usr/bin/env python
'''
A metascons wrapper module for the GNU hello package
'''

import os
from metascons.wrapper import MetaSconsWrapper
from metascons.wrapper.autoconf import AutoconfWrapper

class HelloWrapper(AutoconfWrapper):

    def tarballurl(self):
        urlpatt = 'http://ftp.gnu.org/gnu/hello/hello-%s.tar.gz'
        return urlpatt % self.env['HELLO_VERSION']

    def environment(self):
        inst = self.installdir()

        return {
            'PATH': [os.path.join(inst,'bin')],
            'INFOPATH': [os.path.join(inst,'share/info')],
            'MANPATH': [os.path.join(inst,'share/man')],
            }

    pass

wrapper = HelloWrapper()

