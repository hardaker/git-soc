#!/usr/bin/python

import yaml
import gitSOC.cmd
import gitSOC.managedRepo
import git
import os
import sys

class Info(gitSOC.cmd.Cmd):
    """Dumps information about the registration of the current directory,
    if it has been registered with git-soc (or else say it hasn't been yet).
"""

    def __init__(self, soc, baseargs = {}):
        gitSOC.cmd.Cmd.__init__(self, soc, baseargs)

    def run(self, args):
        linkname = os.getcwd() + "/.git/git-soc.yml"
        
        # read the yaml
        file = open(linkname, "r")
        # XXX: look upward too
        if not file:
            print "Can not find registration information in .git/git-soc.yml"
            exit(1)
            # XXX: search for it instead in the full set

        out = yaml.load(file)
        # should be prettier than this:
        if not out:
            print "could not parse the registration information from .git/git-soc.yml"
            exit(1)

        file = open(linkname, "r")
        for line in file:
            sys.stdout.write(line)

