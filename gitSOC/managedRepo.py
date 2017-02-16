#!/usr/bin/python

import git
import os

class ManagedRepo(git.Repo):

    def __init__(self, path, url = None, repoconfig = {}):
        self._path = path
        self._initialized = False
        self._url = url
        self._config = repoconfig
        
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

    def get_remotes(self):
        repos = self.get_config("remotes", ['origin/master'])
        if not isinstance(repos, list):
            repos = [repos]
        return repos
    
    def get_config(self, name, default = None):
        if name in self._config:
            return self._config[name]
        return default

    def set_config(self, name):
        # XXX: set now and save? just set and move save to different function?
        pass

    def auto_commit(self):
        return self._auto_commit

    def is_dirty(self, index=True, working_tree=True):
        if not self._initialized:
            return False

        return git.Repo.is_dirty(self, index = index, working_tree = working_tree)

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
