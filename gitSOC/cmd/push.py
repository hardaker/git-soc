#!/usr/bin/python

import yaml
import gitSOC.cmd
import argparse
import git
import os

class Push(gitSOC.cmd.Cmd):

    def __init__(self, soc, baseargs = {}):
        gitSOC.cmd.Cmd.__init__(self, soc, baseargs)

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
                    print(x)
                    print("  push result: " + str(x))
                    print("  old: " + str(x[0].old_commit))
                    print("  new: " + str(x[0].remote_ref_string))
                    print("  summary:" + str(x[0].summary))
                    result = str(x[0].summary)
                else:
                    result = "no remote - weird bug"
            except:
                result = "won't: no origin"
            
        print("%-60s %s" % (repo.path(), result))

    def run(self, args):
        self.soc.foreach_repo(self.push, args)
        

