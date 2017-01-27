#!/usr/bin/python

# note: requirse python2-GitPython, not just "GitPython"

import yaml
import gitSOC.cmd
import argparse
import git
import os

class Cmd(gitSOC.cmd.Cmd):

    def __init__(self, soc, baseargs = {}):
        gitSOC.cmd.Cmd.__init__(self, soc, baseargs)

    def parse_args(self, args):
        p = argparse.ArgumentParser(parents=[self.get_global_parse_args()])
        p.add_argument("--seperator", "-s", action="store_true")
        p.add_argument("--ask", "-a",       action="store_true")
        p.add_argument("command", type=str)
        parsed_args = p.parse_args(args = args)
        if 'command' not in parsed_args:
            print "a command to run must be passed"
            exit(1)
        return parsed_args

    def cmd(self, repo, args):
        if args.seperator or args.ask:
            print "--- " + repo.path()

        # interactive 'ask' mode
        if args.ask:
            result = self.pick_one("Run here: ", ['yes', 'no', 'quit'])
            if result == 'n':
                return
            elif result == 'q':
                exit(0)
                
        self.run_cmd(args.command.split(), repo.path())

    def run(self, args):
        self.verbose("running command: " + args.command)
        self.soc.foreach_repo(self.cmd, args)
