#!/usr/bin/python

import yaml
import gitSOC.cmd
import argparse
import git
import os

class Status(gitSOC.cmd.Cmd):

    def __init__(self, soc, baseargs = {}):
        gitSOC.cmd.Cmd.__init__(self, soc, baseargs)

    def print_repo_status(self, repo, otherargs = None):
        state = " "
        if repo.is_dirty():
            state = "d"

        print("%-60s %s" % (repo.path(), state))

    def run(self, args):
        self.soc.foreach_repo(self.print_repo_status)
        

