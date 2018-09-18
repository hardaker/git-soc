import argparse
import subprocess
import os
import re

class Cmd(object):
    def __init__(self, soc, baseargs = {}, description = "", name=""):
        self.baseargs = baseargs
        self.soc = soc
        self.global_parser = None
        self.description = description
        self.name = name
        self._verbose = False
        self.base = ""
        self.regex = None

    def verbose(self, stuff):
        if self._verbose:
            print(stuff)

    def output(self, stuff):
        print(stuff)
        
    def check_clean(self, repo):
        if not repo._initialized:
            return "needs clone"
        if str(repo.active_branch) != "master":
            self.verbose("  clean check: [branch is '" + str(repo.active_branch) + "' and not 'master']")
            return "won't: not master"
        elif repo.is_dirty():
            return "won't: dirty"
        else:
            return "clean"

    def parse_args(self, args):
        p = argparse.ArgumentParser(parents=[self.get_global_parse_args()],
                                    description=self.description,
                                    prog="git-soc " + self.name)
        parsed_args = p.parse_args(args = args)
        self.register_parsed_args(parsed_args)
        return parsed_args

    def get_global_parse_args(self):
        if not self.global_parser:
            global_defaults  = self.soc.parse_global_args()
            self.global_parser = argparse.ArgumentParser(add_help=False,
                                                         description=self.description)
            self.global_parser.add_argument("--base","-B",
                                            default=global_defaults['base'],
                                            help="Directory where YAML config files are found")
            self.global_parser.add_argument("--regex","-R",
                                            help="Regexp to limit repos to use")
            self.global_parser.add_argument("--verbose", "-v",
                                            action="store_true",
                                            help="Verbose mode")
        return self.global_parser


    def register_parsed_args(self, args):
        self.parsed_args = args
        self._verbose = args.verbose
        self.base    = args.base
        self.regex   = args.regex

        if self.regex and not (re.match("^\^",self.regex) or re.match("\$$",self.regex)):
            self.regex = ".*" + self.regex + ".*"

    def run_cmd(self, command, path=None):
        cwd = os.getcwd()
        if path:
            os.chdir(path)
        self.verbose("running '" + command + "' in " + str(path))
        result = os.system(command)
        if path:
            os.chdir(cwd)
        return result

    def pick_one(self, baseprompt, options, default = None):
        prompt = ""
        table = {}
        selected = "_none"

        for option in options:
            first = option[0]
            therest = option[1:]

            prompt = prompt + ", (" + first + ")" + therest
            if default and first == default:
                prompt = prompt + " [default]"
            table[first] = option

        # drop the leading comma and add the prefix
        prompt = baseprompt + prompt[1:] + ": "

        while selected[0] not in table:
            selected = input(prompt)
            if selected == '' and default:
                selected = default
        return selected

    # XXX: might be better in ManagedRepo?
    def maybe_auto_commit(self, repo):
        if (repo.get_config('auto_commit')):
            self.verbose("auto_commit in " + repo.path())
            self.run_cmd(" ".join(['git', 'commit', '-m', 'git-soc autocommit', '-a']), repo.path())
