import argparse
import subprocess
import os

class Cmd(object):
    def __init__(self, soc, baseargs = {}, description = "", name=""):
        self.baseargs = baseargs
        self.soc = soc
        self.global_parser = None
        self.description = description
        self.name = name

    def verbose(self, stuff):
        print stuff

    def parse_args(self, args):
        p = argparse.ArgumentParser(parents=[self.get_global_parse_args()],
                                    description=self.description,
                                    prog="git-soc " + self.name)
        parsed_args = p.parse_args(args = args)
        return parsed_args

    def check_clean(self, repo):
        if str(repo.active_branch) != "master":
            self.verbose("  clean check: [branch is '" + str(repo.active_branch) + "' and not 'master']")
            return "won't: not master"
        elif repo.is_dirty():
            return "won't: dirty"
        else:
            return "clean"

    def get_global_parse_args(self):
        if not self.global_parser:
            global_defaults  = self.soc.parse_global_args()
            self.global_parser = argparse.ArgumentParser(add_help=False,
                                                         description=self.description)
            self.global_parser.add_argument("--base","-B",
                                            default=global_defaults['base'])
        return self.global_parser

    def run_cmd(self, command, path=None):
        cwd = os.getcwd()
        if path:
            os.chdir(path)
        self.verbose("running '" + " ".join(command) + "' in " + path)
        subprocess.call(command)
        if path:
            os.chdir(cwd)

    def pick_one(self, baseprompt, options, default = None):
        prompt = ""
        table = {}
        selected = None

        for option in options:
            first = option[0]
            therest = option[1:]

            prompt = prompt + ", (" + first + ")" + therest
            if default and first == default:
                prompt = prompt + " [default]"
            table[first] = option

        # drop the leading comma and add the prefix
        prompt = baseprompt + prompt[1:] + ": "

        while selected not in table:
            selected = raw_input(prompt)
            if selected == '' and default:
                selected = default
        return selected

    # XXX: might be better in ManagedRepo?
    def maybe_auto_commit(self, repo):
        if (repo.auto_commit()):
            self.verbose("auto_commit in " + repo.path())
            self.run_cmd(['git', 'commit', '-m', 'git-soc autocommit', '-a'], repo.path())
