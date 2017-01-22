#!/usr/bin/python

import yaml
import gitSOC.cmd
import argparse
import git
import os

class Register(gitSOC.cmd.Cmd):

    def __init__(self):
        gitSOC.cmd.Cmd.__init__(self)

    def parse_args(self):
        p = argparse.ArgumentParser()
        p.add_argument("dir", type=str)
        return p.parse_args

    def run(self, args):
        args = self.parse_args()
        repo = git.Repo(os.getcwd())
        print repo
