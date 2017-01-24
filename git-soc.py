#!/usr/bin/python

# XXX: eventually this will be renamed to straight git-soc

import gitSOC
import argparse
import gitSOC.cmd.register
import gitSOC.cmd.status
import sys

soc = gitSOC.GitSOC()
baseargs = soc.parse_global_args()
soc.load_config_directory(baseargs['base'])

args = sys.argv

# pull off the real command
cmd = args[1]

# drop the exec file and the command name
args = args[2:]

if cmd == 'register':
    cmd = gitSOC.cmd.register.Register(soc, baseargs = baseargs)
elif cmd == 'status':
    cmd = gitSOC.cmd.status.Status(soc, baseargs = baseargs)
else:
    print("unknown command: " + cmd)
    exit(1)
    
parsed_args = cmd.parse_args(args)
cmd.run(parsed_args)

