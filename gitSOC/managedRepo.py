#!/usr/bin/python

import git
import os

class ManagedRepo(git.Repo):

    def __init__(self, path, url = None, auto_commit = False):
        self._path = path
        self._initialized = False
        self._url = url
        self._auto_commit = auto_commit

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
    
    def auto_commit(self):
        return self._auto_commit

    def is_dirty(self):
        if not self._initialized:
            return False

        return git.Repo.is_dirty(self)

    def needs_push(self):
        if not self._initialized:
            return False

        head = self.commit()

        try:
            if self.merge_base("origin/master", head)[0] != head:
                return True
        except:
            return True

        return False

    def needs_merge(self):
        if not self._initialized:
            return False

        head = self.commit()
        try:
            origin = self.commit('origin/master')

            if head != origin:
                # if we're the merge base then we're behind
                if self.merge_base(origin, head)[0] == head:
                    return True
        except:
            return True
        
        return False

if __name__ == "__main__":
    mr = ManagedRepo(".")
    print(mr)
    print "dirty: " + str(mr.is_dirty())
