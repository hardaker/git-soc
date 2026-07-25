import gitSOC.cmd.cmd

class AutoAdd:
    """Auto-adds all changed files with a message."""
    def __init__(self, soc):
        self.add = gitSOC.cmd.cmd.Cmd(soc, {})

    def run_hook(self, repo):
        add_configured: str = repo.get_config("auto_add")
        if add_configured:
            self.add_args = self.add.parse_args(["git add ."])
            return self.add.cmd(repo, self.add_args)
        else:
            self.verbose("not running auto_add -- not enabled")
        
