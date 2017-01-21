import managedRepo
import yaml
import os

class GitSOC(object):

    def __init__(self, paths):
        self.repos = []
        for path in paths:
            self.repos.append(managedRepo.ManagedRepo(path))

        print self.repos

    def print_dirty_status(self):
        for repo in self.repos:
            state = "not dirty"
            if repo.is_dirty():
                state = "dirty"

            print("%-60s %s" % (repo.path(), state))


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

        

if __name__ == "__main__":
    mrs = GitSOC(["."])
    print mrs
    mrs.print_dirty_status()    

    mrs.load_config_directory("/home/hardaker/lib/gitrepos.d")
    mrs.print_dirty_status()    
