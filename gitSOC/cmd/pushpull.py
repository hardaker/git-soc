#!/usr/bin/python

import yaml
import gitSOC.cmd
import argparse
import git
import os
import gitSOC.cmd.push
import gitSOC.cmd.pull

class Pushpull(gitSOC.cmd.Cmd):

    def __init__(self, soc, baseargs = {}):
        gitSOC.cmd.Cmd.__init__(self, soc, baseargs,
                                name="pushpull",
                                description="Functionally equivelent to running 'git soc pull ; git soc pull.")

    def run(self, args, *other_args, **kwargs):
        pullcmd = gitSOC.cmd.pull.Pull(self.soc, self.baseargs)
        pushcmd = gitSOC.cmd.push.Push(self.soc, self.baseargs)

        outputs = []
        outputs.append("Pulling: -----------------")
        pullcmd.run(args)
        outputs.extend(pullcmd.return_and_clear_outputs())

        outputs.append("Pushing: -----------------")
        pushcmd.run(args)
        outputs.extend(pushcmd.return_and_clear_outputs())
        return outputs
        

