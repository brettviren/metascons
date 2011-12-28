#!/usr/bin/env python

import os
import platform

def guess_platform():
    if os.environ.has_key('PLATFORM'):
        return os.environ['PLATFORM']
    if os.environ.has_key('CMTCONFIG'):
        return os.environ['CMTCONFIG'] # legacy CMT variable
    
    plat = [platform.system(),
            platform.machine(),
            ''.join(platform.architecture())]

    return '-'.join(plat)

def fix_env(env):
    env['ENV']['PATH'] = env['ENV']['PATH'].split(':')
    for ptype in ['http','ftp','https','all','no']:
        pname = ptype + '_proxy'
        for var in [pname, pname.upper()]:
            val = os.environ.get(var)
            if not val: continue
            env['ENV'][var] = val
            continue
        continue
    return env

if '__main__' == __name__:
    print guess_platform()



