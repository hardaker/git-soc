#!/usr/bin/python

import yaml
import gitSOC.cmd
import argparse
import git
import os

from logging import debug, error, warning, info, basicConfig

class Status(gitSOC.cmd.Cmd):
    """Command class to check the status of all the git repos"""

    def __init__(self, soc, baseargs = {}):
        gitSOC.cmd.Cmd.__init__(self, soc, baseargs)

    def parse_args(self, args):
        p = argparse.ArgumentParser(parents=[self.get_global_parse_args()],
                                    prog="status",
                                    description="Get the status of all the git repositories loaded from 'base'.")
        #p = argparse.ArgumentParser()
        p.add_argument("-d", "--only-dirty", action="store_true",
                       help="Only report repos with something to report")
        p.add_argument("-u", "--untracked", action="store_true",
                       help="Check for untracked files too (slow)")
        parsed_args = p.parse_args(args = args)

        log_level = parsed_args.log_level.upper()
        basicConfig(level=log_level,
                    format="%(levelname)-10s:\t%(message)s")

        self.register_parsed_args(parsed_args)
        return parsed_args

    def print_repo_status(self, repo, args = None):
        dirty = " "
        merge = " "
        push = " "
        index = " "
        untracked = " "
        report = False
        
        if repo.is_dirty():
            dirty = "d"
            report = True
            
        if repo.is_dirty(index=False):
            index = "+"
            report = True
            
        if repo.needs_push(verbose = args.verbose):
            push = ">"
            report = True

        if repo.needs_merge():
            merge = "<"
            report = True

        if 'untracked' in args and args.untracked:
            if repo.untracked_files:
                untracked = "u"
                report = True

        if 'only_dirty' in args and args.only_dirty and not report:
            return

        self.output("%-60s %s%s%s%s%s" % (repo.path(), dirty, index, merge, push, untracked))
        if self._verbose:
            self.output("  %-10s: %s" % ("branch:", repo.active_branch))
            self.output("  %-10s: %s" % ("head:", repo.head))
            self.output("  %-10s: %s" % ("branch:", repo.active_branch))
            try:
                remote = repo.remote()
                if remote:
                    self.output("  %-10s: %s" % ("remote:", remote.name))
            except Exception as e:
                self.output(e)
            except:
                pass

            self.output("  remotes:")
            for remote in repo.remotes:
                self.output("    %-10s" % (remote.name))

        return self.return_and_clear_outputs()

    
    def run(self, args, *other_args, **kwargs):
        self.soc.foreach_repo(self.print_repo_status, args)
        

