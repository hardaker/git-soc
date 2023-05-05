#!/usr/bin/python

import yaml
import gitSOC.cmd
import gitSOC.managedRepo
import git
import os
import sys

from logging import info

class Enable(gitSOC.cmd.Cmd):
    """Enables a repo."""

    def __init__(self, soc, baseargs = {}):
        gitSOC.cmd.Cmd.__init__(self, soc, baseargs)
        self.soc = soc

    def run(self, args, *other_args, **kwargs):
        repo = gitSOC.managedRepo.ManagedRepo()
        repo.set_config('disabled', False)
        repo.save()
        info("repo enabled")
