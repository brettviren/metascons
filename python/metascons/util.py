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

if '__main__' == __name__:
    print guess_platform()



