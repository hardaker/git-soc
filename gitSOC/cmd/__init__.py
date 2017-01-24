
class Cmd(object):
    def __init__(self, soc, baseargs = {}):
        print "init: " + str(baseargs)
        self.baseargs = baseargs
        self.soc = soc

    def verbose(self, stuff):
        print stuff

    def get_config(self, name):
        if self.baseargs and name in self.baseargs:
            return self.baseargs[name]
        return None

    def get_config_path(self, name):
        return self.get_config('base') + "/" + name + ".yml"

    def parse_args(self, args):
        pass

    def check_clean(self, repo):
        if str(repo.active_branch) != "master":
            self.verbose("  clean check: [branch is '" + str(repo.active_branch) + "' and not 'master']")
            return "won't: not master"
        elif repo.is_dirty():
            return "won't: dirty"
        else:
            return "clean"

