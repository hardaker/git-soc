#!/usr/bin/python

import yaml
import gitSOC.cmd
import argparse
import git
import os
from logging import error 


class Pull(gitSOC.cmd.Cmd):

    def __init__(self, soc, baseargs = {}):
        gitSOC.cmd.Cmd.__init__(self, soc, baseargs, name="pull",
                                description = "Runs the equivelent of 'git pull' on every registered repository found in 'base'.\n\nNote: This refused to pull into a directory directory at this time.")

    def pull(self, repo, args = None):

        # check whether or not we have cloned it at all first
        if not os.path.isdir(repo.path()):
            # this has not yet been pulled at all; clone instead

            if not repo.get_config('clone', True):
                self.verbose("config/clone is off; refusing to pull");
                return

            self.verbose("cloning " + repo.url() + " into " + repo.path())
            result = git.Repo.clone_from(repo.url(), repo.path())
            repo.init_repo()
            self.output("%-60s %s" % (repo.path(), "cloned"))
            repo.create_symlink()
            return

        # make sure symlink is there and proper
        repo.create_symlink()

        # check if it's dirty
        result = self.check_clean(repo)

        # maybe do auto commits
        if result == "won't: dirty":
            self.maybe_auto_commit(repo)
            result = self.check_clean(repo)

        # if we're clean, pull away
        if result == "clean":
            for base in repo.get_remotes():
                self.verbose("pulling " + base['name'] + " -> " + repo.path() + ":")
                remote = repo.remote(base['name'])
                if remote:

                    try:
                        # do the actual pull(s)
                        oldcommit = repo.commit()
                        x = remote.pull()
                        newcommit = repo.commit()
                        self.verbose("  pull result: " + str(x))
                        self.verbose("  old: " + str(x[0].old_commit))
                        self.verbose("  new: " + str(x[0].commit))
                        self.verbose("  flags:" + str(x[0].flags))
                        if oldcommit != newcommit:
                            result = str(oldcommit)[0:6] + ".." + str(newcommit)[0:6]
                        else:
                            result = "[up to date]"
                    except Exception as e:
                        error(e)
                        result = "failed"
                    except:
                        result = "failed"

                else:
                    result = "no remote - weird bug"

                self.output("%-60s %s" % (repo.path(), result))
        else:
            self.output("%-60s %s" % (repo.path(), result))

        return self.return_and_clear_outputs()

    def run(self, args, *other_args, **kwargs):
        return self.soc.foreach_repo(self.pull, args)
