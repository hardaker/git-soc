#!/usr/bin/python

import yaml
import gitSOC.cmd
import argparse
import git
import os
from logging import error 


class Run_hooks(gitSOC.cmd.Cmd):

    def __init__(self, soc, baseargs = {}):
        gitSOC.cmd.Cmd.__init__(self, soc, baseargs, name="hooks",
                                description = "Runs all the registered hooks for each repository.  To use these hooks, add 'auto_add: true' and/or 'auto_commit: commit message' to a repos configuration file.")
        self.soc = soc

    def parse_args(self, args):
        p = argparse.ArgumentParser(parents=[self.get_global_parse_args()],
                                    prog="git-soc run_hooks",
                                    description="Runs all the registered hooks for each repository.  To use these hooks, add 'auto_add: true' and/or 'auto_commit: commit message' to a repos configuration file.",
                                    epilog="Example: git soc run_hooks")
        parsed_args = p.parse_args(args = args)
        self.register_parsed_args(parsed_args)
        return parsed_args

    def run_hooks(self, repo, hook):
        if repo.get_config(hook):
            self.verbose(f"Running {hook} in {repo.path}")
            if hook == "auto_commit":  # TODO: ick
                import gitSOC.hooks.auto_commit as autocommit
                hook_obj = autocommit.AutoCommit(self.soc)
                result = hook_obj.run_hook(repo)
            elif hook == "auto_add":  # TODO: ick
                import gitSOC.hooks.auto_add as autoadd
                hook_obj = autoadd.AutoAdd(self.soc)
                result = hook_obj.run_hook(repo)
            else:
                self.error(f"unknown hook: '{hook}'!")
                result = "unknown hook"

            # display the results
            self.output("%-60s %s" % (repo.path(), result))
        else:
            self.verbose(f"skipping {hook} -- not configured")

        return self.return_and_clear_outputs()

    def run(self, args, *other_args, **kwargs):
        hook_list = ["auto_add", "auto_commit"]  # TODO: ick -- make setable
        for hook in hook_list:
            self.verbose(f"running hook:{hook}")
            return self.soc.foreach_repo(self.run_hooks, hook)
