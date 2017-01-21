#!/usr/bin/python

import git

class ManagedRepo(object):

    def __init__(self, path):
        print "path: " + path
        self._repo = git.Repo(path)
        self._path = path
        
    def path(self):
        return self._path

    def is_dirty(self):
        return self._repo.is_dirty()

if __name__ == "__main__":
    mr = ManagedRepo(".")
    print(mr)
    print(mr.repo)
    print "dirty: " + str(mr.repo.is_dirty())
