#!/usr/bin/python


import unittest
import gitSOC
import gitSOC.cmd.register
import gitSOC.cmd.pull
import gitSOC.cmd.push
import gitSOC.cmd.status
import gitSOC.cmd.cmd
import os
import subprocess
import pdb

if os.path.isdir("__test"):
    print "********* nuking"
    subprocess.call(["rm","-rf","__test"])

class gitSocTests(unittest.TestCase):

    def __init__(self, casenames):
        print casenames
        self.inited = False
        unittest.TestCase.__init__(self, casenames)

    def pushd(self, newpath):
        self.pastdirs.append(os.getcwd())

        #print "jumping into " + newpath
        os.chdir(newpath)

    def popd(self):
        if len(self.pastdirs) < 1:
            print "no more  dirs to pop"
            exit(1)

        popeddir = self.pastdirs[-1]
        self.pastdirs = self.pastdirs[:-1]

        #print "popping out to " + popeddir
        os.chdir(popeddir)

    def setup_soc(self):
        self.soc = gitSOC.GitSOC()
        self.baseargs = self.soc.parse_global_args()

    def create_command(self, command):
        cmd = command(self.soc, self.baseargs)
        self.cmd_args = cmd.parse_args(['-B',self.basedir])
        return cmd

    def create_command_and_run(self, command):
        cmd = self.create_command(command)
        print cmd
        print command
        cmd.run(self.cmd_args)

    def setUp(self):
        self.cwd = os.getcwd() + "/"

        self.pastdirs = []
        self.setup_soc()

        # if os.path.isdir("__test"):
        #     print "nuking"
        #     self.remove_tests()
        self.basedir = self.cwd + "__test/base"
        if not os.path.isdir(self.basedir):
            os.makedirs(self.basedir)

        self.repos = [['repo1', 'repo1'], ['repo2', 'repo2'],
                      ['repo1', 'repo1clone'], ['repo2', 'repo2clone']]

    def remove_tests(self):
        #print "cleaning up"
        subprocess.call(["rm","-rf","__test"])

    #def tearDown(self):
        #self.remove_tests()

    def is_repo_correct(self, repo, args):
        #print "testing repo " + repo.path()
        args['me'].assertTrue(repo.path() != "")
        self.count = self.count + 1

    def create_cloned_repo(self, reponame, cloned_to_name = None):
        if not cloned_to_name:
            cloned_to_name = reponame

        if not os.path.isdir("__test/upstreams/" + reponame):
            os.makedirs("__test/upstreams/" + reponame)
        
            self.pushd(self.cwd + "__test/upstreams/" + reponame)
            subprocess.call(["git", "init", "--bare"])
            self.popd()

        self.pushd(self.cwd + "__test/")
        subprocess.call(["git", "clone", "upstreams/" + reponame,
                         cloned_to_name])
        self.popd()
        
        # set up initial content for establishing a base history tree
        if reponame == cloned_to_name:
            self.pushd(self.cwd + "__test/" + cloned_to_name)
            subprocess.call(["touch", "_soc_test"])
            subprocess.call(["git", "add", "_soc_test"])
            subprocess.call(["git", "commit", "-m", "init", "_soc_test"])
            subprocess.call(["git", "push"])
            self.popd()

    def create_file(self, reponame, filename, content, commit = False):
        self.pushd(self.cwd + "__test/" + reponame)
        fileh = open(filename, "w")
        fileh.write(content)
        fileh.close()

        if commit:
            subprocess.call(["git", "add", filename])
            subprocess.call(["git", "commit", "-m", "commiting " + filename])

        self.popd()

    def run_status(self):
        self.create_command_and_run(gitSOC.cmd.status.Status)

    def test_10_register(self):
        reg = gitSOC.cmd.register.Register(self.soc, self.baseargs)

        self.count = 0

        for repo in self.repos:
            basename = repo[0]
            clonename = repo[1]

            print "*** " + basename + " => " + clonename
            self.create_cloned_repo(basename, clonename)

            self.pushd(self.cwd + "__test/" + clonename)
            #print(args)
            args = reg.parse_args(['-B',self.basedir, clonename])
            reg.run(args)

            self.popd()

            self.assertTrue(os.path.isdir("__test/base"))
            self.assertTrue(os.path.isfile("__test/base/" + clonename + ".yml"))

        self.soc.load_config_directory('__test/base', reg)
        
        self.soc.foreach_repo(self.is_repo_correct, { 'me': self })

        self.assertEqual(self.count, 4)

    def test_20_push_then_pull(self):

        push = self.create_command(gitSOC.cmd.push.Push)
        self.soc.load_config_directory('__test/base', self.cmd_args)

        # create some files
        for repo in self.repos:
            basename = repo[0]
            clonename = repo[1]

            self.create_file(clonename, "file_" + clonename,
                             "my content from " + clonename, True)

            
        # push everything out
        push.run(self.cmd_args)

        # check status
        self.run_status()

        # pull everything into the directories
        # push everything out
        self.create_command_and_run(gitSOC.cmd.pull.Pull)

        # check results, should be 2 failed pushes because of conflict
        self.assertTrue(os.path.isfile("__test/repo1clone/file_repo1"))
        self.assertTrue(os.path.isfile("__test/repo2clone/file_repo2"))
        self.assertFalse(os.path.isfile("__test/repo1/file_repo2clone"))
        self.assertFalse(os.path.isfile("__test/repo2/file_repo1clone"))

        self.run_status()
            
        self.create_command_and_run(gitSOC.cmd.push.Push)
        self.create_command_and_run(gitSOC.cmd.pull.Pull)

        # the above falses should be fixed now
        self.run_status()
        self.assertTrue(os.path.isfile("__test/repo1/file_repo1clone"))
        self.assertTrue(os.path.isfile("__test/repo2/file_repo2clone"))


if __name__ == '__main__':
    unittest.main()

