#!/usr/bin/python

import yaml
import gitSOC.cmd
import argparse
import git
import os

class Register(gitSOC.cmd.Cmd):

    def __init__(self, soc, baseargs = {}):
        gitSOC.cmd.Cmd.__init__(self, soc, baseargs)

    def parse_args(self, args):
        p = argparse.ArgumentParser()
        p.add_argument("dir", type=str)
        parsed_arges = p.parse_args(args = args)
        if 'dir' not in args:
            print "a file name to save it in must be passed"
            exit(1)

    def run(self, args):
        args.dir = self.get_config_path(args.dir)
        self.verbose("registering '" + os.getcwd() + "' in '" + args.dir + "'")

        repo = git.Repo(os.getcwd())

        # convert the current repo info into yaml
        output = { 'gitrepos':
                   [{
                       'dir':  str(os.getcwd()),
                       'args': ''
                   }]}
        repodata = output['gitrepos'][0]

        remotes=repo.remotes
        for remote in remotes:
            if remote.name == 'origin':
                urls = remote.urls
                url = urls.next()
                repodata['url'] = str(url)

        # save the yaml
        file = open(args.dir, "w")
        out = yaml.safe_dump(output,default_flow_style=False)
        file.write(out)