#!/usr/bin/python

import git

class ManagedRepo(git.Repo):

    def __init__(self, path):
        print "path: " + path
        git.Repo.__init__(self, path)
        self._path = path
        
    def path(self):
        return self._path

if __name__ == "__main__":
    mr = ManagedRepo(".")
    print(mr)
    print "dirty: " + str(mr.is_dirty())
