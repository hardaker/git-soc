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
        if result == "clean" or result == "won't: dirty":
            try:
                remote = repo.remote()
                if remote:
                    remote.push()
                    result = "pushed"
                else:
                    result = "no remote - weird bug"
            except:
                result = "won't: no origin"
            
        print("%-60s %s" % (repo.path(), result))

    def run(self, args):
        self.soc.foreach_repo(self.push, args)
        

