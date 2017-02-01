#!/usr/bin/python

import yaml
import gitSOC.cmd
import argparse
import git
import os

class Push(gitSOC.cmd.Cmd):

    def __init__(self, soc, baseargs = {}):
        gitSOC.cmd.Cmd.__init__(self, soc, baseargs, name="push",
                                description = "Runs the equivelent of 'git push' in every registered repository found in 'base'.\n\nIf the 'auto_commit' property is true, it will attempt a commit of everything modified before pushing.")

    def push(self, repo, args = None):

        result = self.check_clean(repo)

        # maybe do auto commits
        if result == "won't: dirty":
            self.maybe_auto_commit(repo)
            result = self.check_clean(repo)

        if result == "clean" or result == "won't: dirty":
            try:
                remote = repo.remote()
                if remote:
                    x = remote.push()
                    self.verbose("  push result: " + str(x))
                    self.verbose("  old: " + str(x[0].old_commit))
                    self.verbose("  new: " + str(x[0].remote_ref_string))
                    self.verbose("  summary:" + str(x[0].summary))
                    result = str(x[0].summary)
                else:
                    result = "no remote - weird bug"
            except:
                result = "won't: no origin"
            
        self.output("%-60s %s" % (repo.path(), result))

    def run(self, args):
        self.soc.foreach_repo(self.push, args)
        

