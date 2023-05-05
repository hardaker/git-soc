#!/usr/bin/python

# note: requirse python2-GitPython, not just "GitPython"

import yaml
import gitSOC.cmd
import argparse
import git
import os
from logging import error,info

class Config(gitSOC.cmd.Cmd):

    def __init__(self, soc, baseargs = {}):
        gitSOC.cmd.Cmd.__init__(self, soc, baseargs)

    def parse_args(self, args):
        p = argparse.ArgumentParser(parents=[self.get_global_parse_args()],
                                    prog="git-soc config",
                                    description="Displays stored yaml configuration for repos.",
                                    epilog="Example: git soc cmd ls")
        p.add_argument( "-s", "--set", type=str,
                       help="Update the configuration based on this content")

        p.add_argument("-a", "--all", action="store_true",
                       help="Dump the variables for all repos (not recommended with -s)")
        parsed_args = p.parse_args(args = args)
        self.register_parsed_args(parsed_args)
        return parsed_args

    def dump_file(self, filename):
        with open(filename) as f:
            for line in f:
                self.output("  " + line.rstrip())


    def config(self, repo, args):
        self.output("--- " + repo.path())

        yamlfile=repo.path() + "/.git/git-soc.yml"
        if not os.path.exists(yamlfile):
            error("ERROR: broken (old?) registry -- no git-soc.yml link!!")
            return

        if args.set:
            (variable, value) = args.set.split("=")
            config = repo.set_config(variable, value)
            repo.save()
            info(f"saved {variable} = {value}")
            return self.return_and_clear_outputs()

        self.output("contents of " + yamlfile + ":")
        self.dump_file(yamlfile)
        
        self.output("# other options with their defaults but not yet set:")
        for option in repo.options:
            self.output(f"    # {option}: {repo.get_config(option)}")

        return self.return_and_clear_outputs()
               
    def run(self, args, *other_args, **kwargs):
        if args.all:
            self.soc.foreach_repo(self.config, args)
        outputs = self.config(gitSOC.managedRepo.ManagedRepo(), args)
        self.print_outputs(outputs)
        
