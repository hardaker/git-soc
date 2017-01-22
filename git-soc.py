#!/usr/bin/python

# XXX: eventually this will be renamed to straight git-soc

import gitSOC
import argparse
import gitSOC.cmd.register
import sys

soc = gitSOC.GitSOC()
baseargs = soc.parse_global_args()
print "parsed: " + str(baseargs)

args = sys.argv
# drop the exec command
# pull off the real command
cmd = args[1]
print cmd
print "args: " + str(args)

# drop the exec file and the command name
args = args[2:]
print args


if cmd == 'register':
    cmd = gitSOC.cmd.register.Register(baseargs = baseargs)
else:
    print("unknown command: " + cmd)
    exit(1)
    
cmd.run(args)

