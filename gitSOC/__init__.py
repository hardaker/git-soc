import managedRepo
import yaml
import os

class GitSOC(object):

    def __init__(self, paths = []):
        self.repos = []
        for path in paths:
            self.repos.append(managedRepo.ManagedRepo(path))

        print self.repos

    def print_dirty_status(self):
        self.foreach_repo(self.print_is_dirty)


    def print_is_dirty(self, repo, otherargs = None):
        state = "not dirty"
        if repo.is_dirty():
            state = "dirty"

        print("%-60s %s" % (repo.path(), state))

    def foreach_repo(self, operator, otherargs = None):
        for repo in self.repos:
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
                    self.repos.append(managedRepo.ManagedRepo(repoconfig['dir']))

    def parse_global_args(self):
        baseargs = {
            'base': os.environ['HOME'] + '/lib/gitrepos.d'
        }
        return baseargs
        

if __name__ == "__main__":
    mrs = GitSOC(["."])
    print mrs
    mrs.print_dirty_status()

    baseargs = mrs.parse_global_args()
    mrs.load_config_directory(baseargs['base'])
    mrs.print_dirty_status()    
