import gitSOC.managedRepo
import yaml
import os
import re
from concurrent.futures import ThreadPoolExecutor
import logging


class GitSOC(object):

    def __init__(self, paths = []):
        self.repos = []
        for path in paths:
            self.repos.append(managedRepo.ManagedRepo(path))

    def handle_outputs(self, outputs):
        if isinstance(outputs, list):
            for output in outputs:
                print(output)
        elif isinstance(outputs, str):
            print(outputs)
        elif isinstance(outputs, dict):
            # if they need something in UI thread, bring it
            # back and call it locally
            if 'interrupt' not in outputs:
                raise ValueError("unknown dict type returned from command " + str(outputs))
            result = outputs['interrupt'](*outputs.get('arguments', []))
            if result:
                if isinstance(result, list):
                    handles.append(tpe.submit(*result))
                else:
                    handles.append(tpe.submit(result))
            print(outputs)
        else:
            raise ValueError("unknown type returned from command " + type(outputs))

    def foreach_repo(self, operator, otherargs = None, threaded=True):
        sortedrepos = sorted(self.repos, key=lambda k: k.path())
        if threaded:
            handles = []
            with ThreadPoolExecutor() as tpe:
                for repo in sortedrepos:
                    if not repo.get_config('disabled', False):
                        handles.append(tpe.submit(operator, repo, otherargs))
                for result in handles:
                    outputs = result.result()
                    if 'verbose' in otherargs and otherargs.verbose:
                        print("------- " + repo.path())
                    if outputs:
                        self.handle_outputs(outputs)
        else:
            for repo in sortedrepos:
                if repo.get_config('disabled', False):
                    continue
                if 'verbose' in otherargs and otherargs.verbose:
                    print("------- " + repo.path())
                operator(repo, otherargs)

    def read_yaml_file(self, filepath):
        fh = open(filepath, "r")
        try:
            data = yaml.load(fh, Loader=yaml.FullLoader)
        except:
            data = yaml.load(fh)
        return data

    def load_config_directory(self, directory, cmd):
        for file in os.listdir(directory):
            yaml_file = os.path.join(directory, file)
            if (os.path.isfile(yaml_file) and file[-3:] == "yml"):
                data = self.read_yaml_file(yaml_file)
                for repoconfig in data['gitrepos']:
                    if 'dir' not in repoconfig or 'url' not in repoconfig:
                        print("Error in " + yaml_file)
                        print("both 'dir' and 'url' are required components")
                    else:
                        if cmd.regex is None or re.match(cmd.regex, repoconfig['dir']):
                            self.repos.append(
                                managedRepo.ManagedRepo(
                                    repoconfig['dir'],
                                    repoconfig['url'],
                                    repoconfig,
                                    yaml_file,
                                    self
                                )
                            )
            elif (os.path.isdir(yaml_file)):
                self.load_config_directory(directory + "/" + file, cmd)

    def parse_global_args(self):
        baseargs = {
            'base': os.environ['HOME'] + '/lib/gitrepos.d'
        }
        return baseargs


if __name__ == "__main__":
    mrs = GitSOC(["."])
    print(mrs)
    #mrs.print_dirty_status()

    baseargs = mrs.parse_global_args()
    mrs.load_config_directory(baseargs['base'])
    #mrs.print_dirty_status()    

    print("got: " + mrs.pick_one("pick one", ["apple", "bananna", "Camel"]))
    
