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
        p.add_argument("--push-pull", "--pp", "-p", action="store_true",
                       help="Do a push/pull for each item too")
        parsed_args = p.parse_args(args = args)
        self.register_parsed_args(parsed_args)
        return parsed_args

    def print_header(self, repo, args):
        print("----")
        self.status.print_repo_status(repo, args)

    def interactive(self, repo, args = None):

        # if push-pull, then always print the header
        if args.push_pull:
            self.print_header(repo, args)

        if not repo.is_dirty():
            if args.push_pull:
                self.push.push(repo,args)
                self.pull.pull(repo,args)
            if args.dirty: # we were told to skip non-dirty things
                return

        # iteratively ask what they want to do
        while True:
            self.print_header(repo, args)
            answer = self.pick_one("Cmd: ", ['status','diff','next','push','l-pull', 'quit', 'Shell', 'git status','! cmd'], default='n')
            if answer[0] == 'n':
                return
            elif answer[0] == 's':
                self.status.print_repo_status(repo, args)
            elif answer[0] == 'p':
                self.push.push(repo, args)
            elif answer[0] == 'l':
                self.pull.pull(repo, args)
            elif answer[0] == 'd':
                self.diff.cmd(repo, self.diff_args)
            elif answer[0] == 'g':
                self.gitstatus.cmd(repo, self.gitstatus_args)
            elif answer[0] == 'q':
                exit(0)
            elif answer[0] == "S":
                self.shell.cmd(repo, self.shell_args)
            elif answer[0] == '!':
                print(answer[1:].lstrip().split(" "))
                self.shell.run_cmd(answer[1:].lstrip().split(" "), repo.path())
            else:
                print("unknown option: '" + answer + "'")

        if args.push_pull:
            self.push.push(repo,args)
            self.pull.pull(repo,args)

    def run(self, args):
        self.soc.foreach_repo(self.interactive, args)
