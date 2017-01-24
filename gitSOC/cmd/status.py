#!/usr/bin/python

import yaml
import gitSOC.cmd
import argparse
import git
import os

class Status(gitSOC.cmd.Cmd):

    def __init__(self, soc, baseargs = {}):
        gitSOC.cmd.Cmd.__init__(self, soc, baseargs)

    def parse_args(self, args):
        p = argparse.ArgumentParser()
        p.add_argument("--verbose", "-v",
                       action="store_true",
                       help="Verbose mode")
        parsed_args = p.parse_args(args = args)
        return parsed_args

    def print_repo_status(self, repo, args = None):
        state = " "
        if repo.is_dirty():
            state = "d"

        print("%-60s %s" % (repo.path(), state))
        if args.verbose:
            print("  %-10s: %s" % ("branch:", repo.active_branch))
            print("  %-10s: %s" % ("head:", repo.head))
            print("  %-10s: %s" % ("branch:", repo.active_branch))
            try:
                remote = repo.remote()
                if remote:
                    print("  %-10s: %s" % ("origin:", remote.name))
            except:
                pass

            print "  remotes:"
            for remote in repo.remotes:
                print("    %-10s" % (remote.name))
                
            
    def run(self, args):
        self.soc.foreach_repo(self.print_repo_status, args)
        

