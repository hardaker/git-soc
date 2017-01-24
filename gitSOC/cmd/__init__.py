
class Cmd(object):
    def __init__(self, baseargs = {}):
        print "init: " + str(baseargs)
        self.baseargs = baseargs

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

    
