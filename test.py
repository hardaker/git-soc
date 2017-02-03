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

class gitSocTests(unittest.TestCase):

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

    def setUp(self):
        print "setting up"

        self.pastdirs = []
        self.soc = gitSOC.GitSOC()
        self.baseargs = self.soc.parse_global_args()

        if os.path.isdir("__test"):
            self.remove_tests()
        os.makedirs("__test/repo1")
        os.makedirs("__test/repo2")
        os.makedirs("__test/base")
        
        tmpcmd = gitSOC.cmd.cmd.Cmd(self.soc, self.baseargs)
        tmpcmd.run_cmd(["git", "init"], "__test/repo1")
        tmpcmd.run_cmd(["git", "init"], "__test/repo2")

    def remove_tests(self):
        #print "cleaning up"
        subprocess.call(["rm","-rf","__test"])

    #def tearDown(self):
        #self.remove_tests()

    def is_repo_correct(self, repo, args):
        #print "testing repo " + repo.path()
        args['me'].assertTrue(repo.path() != "")
        self.count = self.count + 1

    def test_register(self):
        cwd = os.getcwd() + "/"
        basedir = cwd + "__test/base"
        reg = gitSOC.cmd.register.Register(self.soc, self.baseargs)

        repos = ['repo1', 'repo2']

        self.count = 0
        for repo in repos:

            self.pushd(cwd + "__test/" + repo)
            args = reg.parse_args(['-B',basedir, repo])
            self.popd()

            #print(args)
            reg.run(args)

            self.assertTrue(os.path.isdir("__test/base"))
            self.assertTrue(os.path.isfile("__test/base/" + repo + ".yml"))

        self.soc.load_config_directory('__test/base', reg)
        
        self.soc.foreach_repo(self.is_repo_correct, { 'me': self })

        self.assertEqual(self.count, 2)

if __name__ == '__main__':
    unittest.main()

