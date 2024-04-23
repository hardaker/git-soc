#!/usr/bin/python3

import gitSOC
import argparse
import importlib
from logging import error
import traceback

import gitSOC.cmd.register
import gitSOC.cmd.status
import gitSOC.cmd.info
import gitSOC.cmd.fetch
import gitSOC.cmd.pull
import gitSOC.cmd.push
import gitSOC.cmd.pushpull
import gitSOC.cmd.interactive
import gitSOC.cmd.cmd
import gitSOC.cmd.config
import gitSOC.cmd.linkup
import gitSOC.cmd.disable
import gitSOC.cmd.enable

import sys

soc = gitSOC.GitSOC()
baseargs = soc.parse_global_args()
aliases = {
    'i': {
        'name': 'interactive'
    },
    'diff': {
        'name': 'cmd',
        'args': ["git diff"]
    },
    'git': {
        'name': 'cmd',
        'args': ['git']
    }
}

args = sys.argv

# pull off the real command
cmd = args[1]

# drop the exec file and the command name
args = args[2:]

# check for help requests first
if cmd == "-h" or cmd == "--help" or cmd == "help":
    print("Usage: " + sys.argv[0] + " COMMAND [-B basedir] <COMMAND ARGS>")
    print("\nCommands available that act on the current repo:")
    print("    " + "\n    ".join(["register","info","config","enable","disable",]))
    print("\nCommands available that act on all repos:")
    print("    " + "\n    ".join(["status","interactive","pull","push","pushpull","command", "enable", "disable"]))
    print("\nSee the --help output of each command for further details")
    exit(0)

try:
    if cmd in aliases:
        if 'args' in aliases[cmd]:
            args = aliases[cmd]['args'] + args
        cmd = aliases[cmd]['name']
        error(cmd)
        error(args)
    module = importlib.import_module(f"gitSOC.cmd.{cmd}")
    cmd = getattr(module, cmd.capitalize())
    cmd = cmd(soc, baseargs = baseargs)
except Exception as ee:
    if isinstance(ee, ModuleNotFoundError):
        error(f"unknown command: {cmd}")
    else:
        print(f"exception: {ee}")
        traceback.print_exc()
    exit(1)
    
parsed_args = cmd.parse_args(args)
soc.load_config_directory(parsed_args.base, cmd)
cmd.run(parsed_args)

