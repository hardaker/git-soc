#!/usr/bin/python

import yaml
import gitSOC.cmd
import gitSOC.managedRepo
import git
import os
import sys

class Fix(gitSOC.cmd.Cmd):
    """(re-)links an existing config file"""

    def __init__(self, soc, baseargs = {}):
        gitSOC.cmd.Cmd.__init__(self, soc, baseargs)
        self.soc = soc

    def run(self, args, *other_args, **kwargs):

        # TODO: move upward until .git
        our_dir = os.getcwd()

        saved_repo = None
        for repo in self.soc.repos:
            if repo.get_config('dir') == our_dir:
                saved_repo = repo

        print(f"checked and found: {saved_repo}")

        if saved_repo.check_symlink():
            print("error found: symlink incorrect or missing -- fixed")
            yaml_file = saved_repo.get_config_path()  # need to fix this

