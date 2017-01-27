import managedRepo
import yaml
import os

class GitSOC(object):

    def __init__(self, paths = []):
        self.repos = []
        for path in paths:
            self.repos.append(managedRepo.ManagedRepo(path))

    def foreach_repo(self, operator, otherargs = None):
        sortedrepos = sorted(self.repos, key=lambda k: k.path())
        for repo in sortedrepos:
            operator(repo, otherargs)
        

    def read_yaml_file(self, filepath):
        fh = open(filepath, "r")
        data = yaml.load(fh)
        return data

    def load_config_directory(self, directory):
        for file in os.listdir(directory):
            if (os.path.isfile(directory + "/" + file) and file[-3:] == "yml"):
                data = self.read_yaml_file(directory + "/" + file)
                for repoconfig in data['gitrepos']:
                    if 'dir' not in repoconfig or 'url' not in repoconfig:
                        print("Error in " + directory + "/" + file)
                        print("both 'dir' and 'url' are required components")
                    else:
                        auto_commit = False
                        if 'auto_commit' in repoconfig:
                            auto_commit = repoconfig['auto_commit']
                        self.repos.append(managedRepo.ManagedRepo(repoconfig['dir'],
                                                                  repoconfig['url'],
                                                                  auto_commit))
            elif (os.path.isdir(directory + "/" + file)):
                self.load_config_directory(directory + "/" + file)

    def parse_global_args(self):
        baseargs = {
            'base': os.environ['HOME'] + '/lib/gitrepos.d'
        }
        return baseargs
        
    def pick_one(self, baseprompt, options):
        prompt = ""
        table = {}
        selected = None

        for option in options:
            first = option[0]
            therest = option[1:]
            prompt = prompt + ", (" + first + ")" + therest
            table[first] = option

        # drop the leading comma and add the prefix
        prompt = baseprompt + prompt[1:] + ": "

        while selected not in table:
            selected = raw_input(prompt)
        return selected

if __name__ == "__main__":
    mrs = GitSOC(["."])
    print mrs
    #mrs.print_dirty_status()

    baseargs = mrs.parse_global_args()
    mrs.load_config_directory(baseargs['base'])
    #mrs.print_dirty_status()    

    print "got: " + mrs.pick_one("pick one", ["apple", "bananna", "Camel"])
