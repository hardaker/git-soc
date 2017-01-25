import argparse

class Cmd(object):
    def __init__(self, soc, baseargs = {}):
        self.baseargs = baseargs
        self.soc = soc
        self.global_parser = None

    def verbose(self, stuff):
        print stuff

    def parse_args(self, args):
        parser = self.get_global_parse_args()
        args = parser.parse_args(args)
        return args

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
            self.global_parser = argparse.ArgumentParser(add_help=False)
            self.global_parser.add_argument("--base","-B",
                                            default=global_defaults['base'])
        return self.global_parser

