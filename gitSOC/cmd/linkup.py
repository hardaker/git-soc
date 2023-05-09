#!/usr/bin/python

# note: requirse python2-GitPython, not just "GitPython"

import yaml
import gitSOC.cmd
import argparse
import git
import os

class Linkup(gitSOC.cmd.Cmd):

    def __init__(self, soc, baseargs = {}):
        gitSOC.cmd.Cmd.__init__(self, soc, baseargs)

    def linkup(self, repo, args):
        repo.check_symlink(create = True)

    def run(self, args, *other_args, **kwargs):
        self.soc.foreach_repo(self.linkup, args)
