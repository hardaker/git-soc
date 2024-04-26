#!/usr/bin/python

import yaml
import git
import os
import traceback
from logging import error, debug, warning


class ManagedRepo(git.Repo):

    def __init__(self, path = None, url = None, repoconfig = {}, yaml_file = None, soc = None):
        self._path = path or os.getcwd()
        self._initialized = False
        self._url = url
        self._config = repoconfig
        self._current_command = None
        self.yaml_file = yaml_file
        self.soc = soc

        self._options = {
            'disabled': False,
            'remotes': 'origin/main',
            'active_branches': 'main,master',
        }

        self.init_repo()

    @property
    def options(self):
        return self._options

    @property
    def config_file(self):
        # if not self.check_symlink():
        #     error("unable to locate git-soc config")
        return self.get_config_path()

    @property
    def path(self):
        return self._path

    @property
    def current_command(self):
        """The current command object being used.

        This is mostly useful for using erro/warning in threads"""
        return self._current_command

    def error(self, msg):
        if self.current_command:
            self.current_command.error(msg)
        else:
            error(msg)

    def warning(self, msg):
        if self.current_command:
            self.current_command.warning(msg)
        else:
            warning(msg)

    def output(self, msg):
        if self.current_command:
            self.current_command.output(msg)
        else:
            print(msg)
            
    @current_command.setter
    def current_command(self, new_current_command):
        self._current_command = new_current_command

    def load(self, filepath: str = None):
        if not filepath:
            filepath = self.config_file

        fh = open(filepath, "r")
        try:
            data = yaml.load(fh, Loader=yaml.FullLoader)
        except:
            data = yaml.load(fh)
        self._config = data
        return data

    def save(self, save_path = None, config = None):

        if not config:
            config = self._config
        if not save_path:
            save_path = self.config_file
            
        # create the directory structure if needed
        if not os.path.isdir(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))
            
        file = open(save_path, "w")
        out = yaml.safe_dump(config,default_flow_style=False)
        file.write(out)

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

        if not self._config and self._path:
            self.load()

        return self._initialized

    def path(self):
        return self._path

    def url(self):
        return self._url

    def get_remotes(self):
        repos = self.get_config("remotes")
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
        return self._config.get(name, default or self.options.get(name))

    def set_config(self, name, value):
        self._config['gitrepos'][0][name] = value
        # XXX: set now and save? just set and move save to different function?
        pass

    def is_dirty(self, index=True, working_tree=True):
        if not self._initialized:
            return False

        return git.Repo.is_dirty(self, index = index, working_tree = working_tree)

    def check_active_branch(self):
        """checks to see if the current branch is an active branch or not

        returns False when its not, or the (str) active branch name when it is
        """
        branches = self.get_config("active_branches").split(",")
        active_branch = str(self.active_branch)
        if active_branch not in branches:
            self.warning(f"checked out branch {active_branch} is not in active_branches: {branches}")
            return False
        return active_branch
        
    def needs_push(self, verbose = False):
        """Returns True if the checkout needs to be pushed"""
        if not self._initialized:
            return False

        remotes = self.get_remotes()
        result = False
        active_branch = self.check_active_branch()
        if not active_branch:
            return False

        for remote in remotes:
            try:
                head = self.commit()
                merge_base = self.merge_base(remote['name'] + "/" + active_branch, head)[0]
                if verbose:
                    print(" cur head:   " + head)
                    print(" merge_base: " + merge_base)

                if merge_base != head:
                    result = True
            except:
                result = True

        return result

    def needs_merge(self):
        """Returns True if the checkout needs to be merged with an upstream"""
        if not self._initialized:
            return False

        for remote in self.get_remotes():
            try:
                head = self.commit()
                active_branch = self.check_active_branch()
                if not active_branch:
                    return True
                
                origin = self.commit(remote['name'] + "/" + active_branch)

                if head != origin:
                    # if we're the merge base then we're behind
                    if self.merge_base(origin, head)[0] == head:
                        return True
                    # if neither is, then we're diverged and need merge
                    elif self.merge_base(origin, head)[0] != origin:
                        return True
            except Exception as e:
                self.error(f"needs_merge failed for {self._path}: {e}")
                debug(traceback.format_exc())
                return True

        return False

    def create_symlink(self):
        our_dir = self.get_config('dir') 
        linkname = os.path.join(our_dir, ".git", "git-soc.yml")

        # create a sym link
        save_name = self.get_config('name')

        # find where we should link to
        if not save_name:
            for repo in self.soc.repos:
                if repo.get_config('dir') == our_dir:
                    save_name = repo.yaml_file

        if not os.path.islink(linkname) and save_name != None:
            if save_name[:3] == "../":
                # relative link add in another ../
                save_name = "../" + save_name
            os.symlink(save_name, linkname)

    def get_config_path(self):
        repodir = self.get_config('dir') or self._path
        linkname = os.path.join(repodir, ".git", "git-soc.yml")
        return linkname

    def check_symlink(self, create = True):
        if not self.is_initialized():
            return False

        # print(self)
        repodir = self.get_config('dir') or self._path
        name = self.get_config('name')
        linkname = repodir + "/.git/git-soc.yml"

        # ensure this repo isn't registered somewhere
        if os.path.islink(linkname):
            self.output("repository already registered; not re-linking")
            self.output("  see link:    '" + linkname + "'")
            self.output("  pointing to: '" + os.path.realpath(linkname) + "'")
            return False

        if os.path.isdir(linkname) or os.path.isfile(linkname):
            self.error(linkname + " exists but isn't a symlink")
            return False

        # ensure this registration doesn't exist yet 
        if name and os.path.isfile(name):
            self.error(name + "' already exists")
            return False

        # create a sym link
        self.warning("symlink missing: " + linkname)
        if create:
            self.output("will try to create it")
            self.create_symlink()

        return True

    def is_initialized(self):
        return self._initialized

if __name__ == "__main__":
    mr = ManagedRepo(".")
    print(mr)
    print("dirty: " + str(mr.is_dirty()))
