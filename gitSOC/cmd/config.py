#!/usr/bin/python

# note: requirse python2-GitPython, not just "GitPython"

import yaml
import gitSOC.cmd
import argparse
import git
import os

class Config(gitSOC.cmd.Cmd):

    def __init__(self, soc, baseargs = {}):
        gitSOC.cmd.Cmd.__init__(self, soc, baseargs)

    def parse_args(self, args):
        p = argparse.ArgumentParser(parents=[self.get_global_parse_args()],
                                    prog="git-soc config",
                                    description="Displays stored yaml configuration for repos.",
                                    epilog="Example: git soc cmd ls")
        p.add_argument("--set", "-s", type=argparse.FileType("r"),
                       help="Update the configuration based on this content")
        parsed_args = p.parse_args(args = args)
        self.register_parsed_args(parsed_args)
        return parsed_args

    def dump_file(self, filename):
        with open(filename) as f:
            for line in f:
                print("  " + line.rstrip())


    def config(self, repo, args):
        print("--- " + repo.path())

        yamlfile=repo.path() + "/.git/git-soc.yml"
        if os.path.exists(yamlfile):
            self.dump_file(yamlfile)
        else:
            print("ERROR: no git-soc.yml link!!")
               
    def run(self, args):
        self.soc.foreach_repo(self.config, args)
