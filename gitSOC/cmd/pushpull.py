#!/usr/bin/python

import yaml
import gitSOC.cmd
import argparse
import git
import os
import gitSOC.cmd.push
import gitSOC.cmd.pull

class PushPull(gitSOC.cmd.Cmd):

    def __init__(self, soc, baseargs = {}):
        gitSOC.cmd.Cmd.__init__(self, soc, baseargs,
                                name="pushpull",
                                description="Functionally equivelent to running 'git soc pull ; git soc pull.")

    def run(self, args):
        pullcmd = gitSOC.cmd.pull.Pull(self.soc, self.baseargs)
        pushcmd = gitSOC.cmd.push.Push(self.soc, self.baseargs)

        print "Pulling: -----------------"
        pullcmd.run(args)
        print "\nPushing: -----------------"
        pushcmd.run(args)
        

