#!/usr/bin/python

# note: requirse python2-GitPython, not just "GitPython"

import yaml
import gitSOC.cmd
import gitSOC.managedRepo
import argparse
import git
import os

class Register(gitSOC.cmd.Cmd):
    """Command class to register new repos within the base directory

    This creates a new yml file for the registered repo/directory/name"""

    def __init__(self, soc, baseargs = {}):
        gitSOC.cmd.Cmd.__init__(self, soc, baseargs)

    def parse_args(self, args):
        p = argparse.ArgumentParser(parents=[self.get_global_parse_args()],
                                    prog="git-soc register",
                                    description="Registers the current git repository as a new YAML file in the 'base' directory (defaults to ~/lib/gitrepos.d).  Requires a name, which .yml will be appended to before saving.")
        p.add_argument("name", type=str,
                       help="The name to save the YAML file as; it may contain subdirectory path like foo/bar")
        p.add_argument("-r", "--remote", type=str, default="origin",
                       help="The name of the remote (default: 'origin')")
        parsed_args = p.parse_args(args = args)
        self.register_parsed_args(parsed_args)
        if 'name' not in parsed_args:
            print("a file name to save it in must be passed")
            exit(1)
        return parsed_args

    def run(self, args):
        args.name = args.base + "/" + args.name + ".yml"

        # create a real repo to have it figure out the true base path
        repo = git.Repo(os.getcwd())
        basepath = str(repo.working_tree_dir)
        if not basepath:
            print("unable to figure out a top base path for this supposed repo")
            exit(1)

        # convert the current repo info into yaml
        output = { 'gitrepos':
                   [{
                       'dir':    basepath,
                       'args':   '',
                       'remote': args.remote,
                       'name':   args.name,
                   }]}
        repodata = output['gitrepos'][0]

        repo = gitSOC.managedRepo.ManagedRepo(basepath, repoconfig = repodata)


        # ensure this repo isn't registered somewhere
        if repo.check_symlink(create = False) == False:
            return

        remotes=repo.remotes
        for remote in remotes:
            if remote.name == args.remote:
                urls = remote.urls
                url = next(urls)
                repodata['url'] = str(url)

        if 'url' not in repodata:
            print("unable to register this repository -- it has no remote '" +
                  args.remote + "'")
            exit(1)

        # save the yaml
        repo.save()

        # create a sym link
        repo.create_symlink()

        self.verbose("-- registering '" + os.getcwd() + "' in '" + args.name + "'")
