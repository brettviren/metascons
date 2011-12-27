#!/usr/bin/env python
'''
Wrap up building python.  Clearly a chicken and egg thing, this relies
on the system python to run.
'''

import os
from metascons.wrapper.autoconf import AutoconfWrapper

class PythonWrapper(AutoconfWrapper):

    def name(self):
        return 'Python'         # capitalized

    def tarballname(self):
        return '%s-%s.tgz' % (self.name(), self.env['PYTHON_VERSION'])

    def tarballurl(self):
        urlpatt = 'http://python.org/ftp/python/%s/%s'
        return urlpatt % (self.env['PYTHON_VERSION'], self.tarballname())

    pass


wrapper = PythonWrapper()



