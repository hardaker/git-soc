#!/usr/bin/python

import yaml
import gitSOC.cmd
import argparse
import git
import os

class Fetch(gitSOC.cmd.Cmd):

    def __init__(self, soc, baseargs = {}):
        gitSOC.cmd.Cmd.__init__(self, soc, baseargs, name="pull",
                                description = "Runs the equivelent of 'git pull' on every registered repository found in 'base'.\n\nNote: This refused to pull into a directory directory at this time.")

    def fetch(self, repo, args = None):
        # check whether or not we have cloned it at all first
        if not os.path.isdir(repo.path()):
            print("%-60s %s" % (repo.path(), "needs clone"))
            return

        try:
            # do the actual fetch
            remote = repo.remote()
            self.verbose("fetching " + repo.path() + ":")
            if remote:
                oldcommit = remote.commit()
                x = remote.fetch()
                newcommit = remote.commit()
                self.verbose("  fetch result: " + str(x))
                self.verbose("  old: " + str(x[0].old_commit))
                self.verbose("  new: " + str(x[0].commit))
                self.verbose("  flags:" + str(x[0].flags))
                if oldcommit != newcommit:
                    result=oldcommit[0:6] + ".." + newcommit[0:6]
                else:
                    result = "[up to date]"
            else:
                result = "no remote - weird bug"
        except:
            result = "fail - crashed"
            
        print("%-60s %s" % (repo.path(), result))

    def run(self, args):
        self.soc.foreach_repo(self.fetch, args)
        

