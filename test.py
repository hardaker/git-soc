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
            print "nuking"
            self.remove_tests()
        os.makedirs("__test/base")

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

        cwd = os.getcwd() + "/"
        if not os.path.isdir("__test/upstreams/" + reponame):
            os.makedirs("__test/upstreams/" + reponame)
        
            self.pushd(cwd + "__test/upstreams/" + reponame)
            subprocess.call(["git", "init"])
            self.popd()

        self.pushd(cwd + "__test/")
        subprocess.call(["git", "clone", "upstreams/" + reponame,
                         cloned_to_name])
        self.popd()
        
    def test_register(self):
        cwd = os.getcwd() + "/"
        basedir = cwd + "__test/base"
        reg = gitSOC.cmd.register.Register(self.soc, self.baseargs)

        repos = [['repo1', 'repo1'], ['repo2', 'repo2'],
                 ['repo1', 'repo1clone'], ['repo2', 'repo2clone']]

        self.count = 0
        for repo in repos:

            self.create_cloned_repo(repo[0], repo[1])
            args = reg.parse_args(['-B',basedir, repo[1]])

            self.pushd(cwd + "__test/" + repo[1])
            args = reg.parse_args(['-B',basedir, repo[1]])
            #print(args)
            reg.run(args)

            self.popd()

            self.assertTrue(os.path.isdir("__test/base"))
            self.assertTrue(os.path.isfile("__test/base/" + repo[1] + ".yml"))

        self.soc.load_config_directory('__test/base', reg)
        
        self.soc.foreach_repo(self.is_repo_correct, { 'me': self })

        self.assertEqual(self.count, 4)

if __name__ == '__main__':
    unittest.main()

