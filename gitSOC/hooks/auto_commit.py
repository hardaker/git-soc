import gitSOC.cmd.cmd

class AutoCommit:
    """Auto-commits all changed files with a message."""
    def __init__(self, soc):
        self.commit = gitSOC.cmd.cmd.Cmd(soc, {})

    def run_hook(self, repo):
        commit_string: str = repo.get_config("auto_commit")
        if commit_string:
            self.commit_args = self.commit.parse_args(["git commit -a -m '" + commit_string + "'"])
            return self.commit.cmd(repo, self.commit_args)
        else:
            self.verbose("not running auto_commit -- not enabled")
        
