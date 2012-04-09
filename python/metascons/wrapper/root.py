#!/usr/bin/env python
'''
Wrap up the building of ROOT
'''

import os
from metascons.wrapper.autoconf import AutoconfWrapper

# not really autoconf but ROOT uses a configure script
class RootWrapper(AutoconfWrapper):

    def dependencies(self):
        return ['python']

    def prepare_options(self):
        'Options sent to configure'
        from metascons.wrapper import python as mwp
        inst = mwp.wrapper.installdir()

        return '--with-python-incdir=%s/include --with-python-libdir=%s/lib' % \
            (inst,inst)

    def tarballname(self):
        return 'root_v%s.source.tar.gz' % self.env['ROOT_VERSION']

    def tarballurl(self):
        urlpatt = 'ftp://root.cern.ch/root/%s'
        return urlpatt % self.tarballname()

    def unpack_action(self):
        "Root's tarball unpacks to just root/"
        act = AutoconfWrapper.unpack_action(self)
        cmds = act.split('&&')
        mvcmd = 'mv root/* %s && rmdir root ' % self.sourcedir()
        cmds.insert(-1, mvcmd)
        ret = ' && '.join(cmds)
        print ret
        return ret

    pass


wrapper = RootWrapper()

