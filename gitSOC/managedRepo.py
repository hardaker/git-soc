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

        final_repos = []
        for repo in repos:
            details = repo.split("/")
            final_repos.append({ 'name': details[0],
                                 'branch': details[1] })

        # XXX: error checking for all parts

        return final_repos
    
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

    def needs_push(self, verbose = False):
        if not self._initialized:
            return False

        remotes = self.get_remotes()
        result = False

        for remote in remotes:
            try:
                head = self.commit()
                merge_base = self.merge_base(remote['name'] + "/" + remote['branch'], head)[0]
                if verbose:
                    print " cur head:   " + head
                    print " merge_base: " + merge_base

                if merge_base != head:
                    result = True
            except:
                result = True

        return result

    def needs_merge(self):
        if not self._initialized:
            return False

        for remote in self.get_remotes():
            try:
                head = self.commit()
                origin = self.commit(remote['name'] + "/" + remote['branch'])

                if head != origin:
                    # if we're the merge base then we're behind
                    if self.merge_base(origin, head)[0] == head:
                        return True
            except:
                print "ERROR: needs_merge failed"
                return True
        
        return False

    def create_symlink(self):
        linkname = self.get_config('dir') + "/.git/git-soc.yml"

        # create a sym link
        save_name = self.get_config('name')
        if not os.path.islink(linkname) and save_name != None:
            if save_name[:3] == "../":
                # relative link add in another ../
                save_name = "../" + save_name
            os.symlink(save_name, linkname)
        
    def check_symlink(self, create = True):
        if not self.is_initialized():
            return False

        print self
        repodir = self.get_config('dir')
        name = self.get_config('name')
        linkname = repodir + "/.git/git-soc.yml"

        # ensure this repo isn't registered somewhere
        if os.path.islink(linkname):
            print("error:       repository already registered; refusing to reregister")
            print("see link:    '" + repodir + "/.git/git-soc.yml'")
            print("pointing to: '" + os.path.realpath(linkname) + "'")
            return False

        if os.path.isdir(linkname) or os.path.isfile(linkname):
            print("error: '" + linkname + " exists but isn't a symlink")
            return False

        # ensure this registration doesn't exist yet 
        if os.path.isfile(name):
            print("error: '" + name + "' already exists")
            return False

        # create a sym link
        if create:
            self.create_symlink(repodata)

        return True

    def is_initialized(self):
        return self._initialized

if __name__ == "__main__":
    mr = ManagedRepo(".")
    print(mr)
    print "dirty: " + str(mr.is_dirty())
