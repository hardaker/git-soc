#!/usr/bin/python

import yaml
import gitSOC.cmd
import argparse
import git
import os

import gitSOC.cmd.status
import gitSOC.cmd.info
import gitSOC.cmd.fetch
import gitSOC.cmd.pull
import gitSOC.cmd.push

class Interactive(gitSOC.cmd.Cmd):

    def __init__(self, soc, baseargs = {}):
        gitSOC.cmd.Cmd.__init__(self, soc, baseargs, name="interactive",
                                description = "Walks through all directories and prompts for things to do.")

        self.soc = soc
        self.pull = gitSOC.cmd.pull.Pull(soc, baseargs)
        self.push = gitSOC.cmd.push.Push(soc, baseargs)
        self.status = gitSOC.cmd.status.Status(soc, baseargs)
        self.cmd = gitSOC.cmd.cmd.Cmd(soc, baseargs)

        self.diff = gitSOC.cmd.cmd.Cmd(soc, baseargs)
        self.diff_args = self.diff.parse_args(["git diff"])

        self.shell = gitSOC.cmd.cmd.Cmd(soc, baseargs)
        self.shell_args = self.shell.parse_args(["bash"])

        self.gitstatus = gitSOC.cmd.cmd.Cmd(soc, baseargs)
        self.gitstatus_args = self.shell.parse_args(["git status"])

    def parse_args(self, args):
        p = argparse.ArgumentParser(parents=[self.get_global_parse_args()],
                                    prog="git-soc cmd",
                                    description="Interactively asks for what to do in each repo",
                                    epilog="Example: git soc interactive")
        p.add_argument("--dirty", "-d", action="store_true",
                       help="Only stop into the dirty repos")
        parsed_args = p.parse_args(args = args)
        self.register_parsed_args(parsed_args)
        return parsed_args

    def interactive(self, repo, args = None):
        if args.dirty and not repo.is_dirty():
            return
        
        print("----")
        self.status.print_repo_status(repo, args)

        while True:
            answer = self.pick_one("Cmd: ", ['status','diff','next','p-push','l-pull', 'quit', '!shell', 'git status'], default='n')
            if answer == 'n':
                return
            elif answer == 's':
                self.status.print_repo_status(repo, args)
            elif answer == 'p':
                self.push.push(repo, args)
            elif answer == 'l':
                self.pull.pull(repo, args)
            elif answer == 'd':
                self.diff.cmd(repo, self.diff_args)
            elif answer == 'g':
                self.gitstatus.cmd(repo, self.gitstatus_args)
            elif answer == 'q':
                exit(0)
            elif answer == '!':
                self.shell.cmd(repo, self.shell_args)
            else:
                print("unknown option: '" + answer + "'")

    def run(self, args):
        self.soc.foreach_repo(self.interactive, args)
