#!/usr/bin/python

import yaml
import gitSOC.cmd
import argparse
import git
import os

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
            
        if repo.needs_push():
            push = ">"
            report = True

        if repo.needs_merge():
            merge = "<"
            report = True

        if args.untracked:
            if repo.untracked_files:
                untracked = "u"
                report = True

        if args.only_dirty and not report:
            return

        print("%-60s %s%s%s%s%s" % (repo.path(), dirty, index, merge, push, untracked))
        if self._verbose:
            print("  %-10s: %s" % ("branch:", repo.active_branch))
            print("  %-10s: %s" % ("head:", repo.head))
            print("  %-10s: %s" % ("branch:", repo.active_branch))
            try:
                remote = repo.remote()
                if remote:
                    print("  %-10s: %s" % ("remote:", remote.name))
            except Exception as e:
                print e
            except:
                pass

            print "  remotes:"
            for remote in repo.remotes:
                print("    %-10s" % (remote.name))
                
            
    def run(self, args):
        self.soc.foreach_repo(self.print_repo_status, args)
        

