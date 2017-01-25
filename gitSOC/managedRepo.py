#!/usr/bin/python

import git
import os

class ManagedRepo(git.Repo):

    def __init__(self, path, url = None):
        self._path = path
        self._initialized = False
        self._url = url
        self.init_repo()

    def init_repo(self):
        """
        Initializes our parent git.Repo() based on the working path if it exists.

        This is generally safe to call multiple times, as it won't initialize
        more than once."""
        if self._initialized:
            return True

        if os.path.isdir(self._path):
            self._initialized = True
            git.Repo.__init__(self, self._path)

        return self._initialized

    def path(self):
        return self._path

    def url(self):
        return self._url
    
if __name__ == "__main__":
    mr = ManagedRepo(".")
    print(mr)
    print "dirty: " + str(mr.is_dirty())
