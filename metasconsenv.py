#!/usr/bin/env python
'''
Generate environment settings based on a the environment file produced
by "metascons --environment-file=foo.txt"

This script is meant to be run from a sh function or csh alias.  See
mscenv.sh/.csh for examples.
'''

import os
import sys
import optparse
from metascons.util import merge_dict

usage = 'usage: %prog [options] env.txt [...]'
parser = optparse.OptionParser(usage=usage)
parser.add_option('-s','--shell', default='sh',
                  help='The shell to generate for (def=sh)')
#parser.add_option('-u','--unset', default=False, action='store_true',
#                  help='Unset the environment instead of setting it')
(opts,args) = parser.parse_args()

if not args:
    parser.print_help()
    sys.stderr.write('No environment files given\n')
    sys.exit(1)

# Slurp in env files
env = {}
for envfile in args:
    fp = open(envfile)
    code = fp.read()
    #print code
    other_env = eval(code)
    merge_dict(env,other_env)
    continue

# Get any user env that will be stepped on 
user = {}
for key in env.keys():
    user[key] = os.environ.get(key)

# Merge the two and flatten any lists to strings
merge_dict(user,env)
for key,val in user.iteritems():
    if type(val) == list:
        user[key] = ':'.join(val)
        pass
    continue

def sh_munger(theenv):
    for key,val in theenv.iteritems():
        print 'export %s="%s"' % (key,val)
        continue
    return
def cs_munger(theenv):
    for key,val in theenv.iteritems():
        print 'setenv %s "%s"' % (key,val)
        continue
    return

envmunger = None
if opts.shell.lower() in ['sh','bash']:
    envmunger = sh_munger
if opts.shell.lower() in ['csh','tcsh']:
    envmunger = cs_munger
if not envmunger:
    parser.print_help()
    sys.stderr.write('Unknown shell: "%s"\n' % opts.shell)
    sys.exit(1)
envmunger(user)

