#!/usr/bin/python

import yaml
import gitSOC.cmd
import argparse
import git
import os

class Pull(gitSOC.cmd.Cmd):

    def __init__(self, soc, baseargs = {}):
        gitSOC.cmd.Cmd.__init__(self, soc, baseargs)

    def pull(self, repo, args = None):
        result = self.check_clean(repo)
        if result is "clean":
            try:
                remote = repo.remote()
                print "pulling...."
                if remote:
                    x = remote.pull()
                    print("  pull result: " + str(x))
                    print("  old: " + str(x[0].old_commit))
                    print("  new: " + str(x[0].commit))
                    print("  flags:" + str(x[0].flags))
                    result = "pulled"
                else:
                    result = "no remote - weird bug"
            except:
                result = "won't ; no origin"
            
        print("%-60s %s" % (repo.path(), result))

    def run(self, args):
        self.soc.foreach_repo(self.pull, args)
        

