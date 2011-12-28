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
    '''
    Fix up the construction environment.  
    '''

    # make sure all PATH variables are lists.
    for key,val in env.Dictionary().iteritems():
        if len(key) < 4 or key[-4:] != 'PATH':
            continue
        if type(val) == str:
            env[key] = val.split(':')
        continue

    # Pass through some proxy related variables from user's
    # environment
    for ptype in ['http','ftp','https','all','no']:
        pname = ptype + '_proxy'
        for var in [pname, pname.upper()]:
            val = os.environ.get(var)
            if not val: continue
            env['ENV'][var] = val
            continue
        continue
    return env

def merge_env(dst,src):
    '''
    Merge the src construction environment into the dst.  This merges
    both the top level env variables and those in the run time env.ENV
    variables.

    For PATH variables, the src list is prepended to the dst list.

    For all others dst retains its variables' values and only
    variables in src that are not in dst are copied over.
    '''

    def merge_dict(d,s):
        for key,val in s.iteritems():

            if key == 'ENV':
                merge_dict(d['ENV'],s['ENV'])

            if not d.has_key(key):
                d[key] = val
                continue

            if len(key) < 4 or key[-4:] != 'PATH':
                continue        # keep d's variable value

            # prepend, respecting if is string or list
            stringify = False
            lhs = d[key]
            if type(lhs) == str:
                stringify = True
                lhs = lhs.split(':')
                pass
            if type(val) == str:
                val = val.split(':')
                pass

            toadd = []
            for thing in val:
                toadd.append(thing)
                if thing in lhs:
                    lhs.remove(thing)
                    pass
                continue
            lhs = toadd + lhs

            if stringify:
                lhs = ':'.join(lhs)

            d[key] = lhs
            continue
        return
            
    merge_dict(dst.Dictionary(), src.Dictionary())
    return

def recursive_merge_env(pobj):
    '''
    Descend any dependencies of the given package object and merge_env
    their .env environments
    '''
    for dep in pobj.depobjs:
        recursive_merge_env(dep)
        merge_env(pobj.env,dep.env)
        continue

def resolve_packages(pkgs):
    if type(pkgs) == list:
        pkgs = ' '.join(pkgs)
    return pkgs.split(' ')



if '__main__' == __name__:
    print guess_platform()

    


