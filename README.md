# Design Goal

I wanted a tool to help manage logging into lots of systems with lots
of files and tools that need to be in lots of places.  But some
systems are for work, others for play, others for photography, etc.
And a different collection of files are needed on each system.  How
can I manage some systems that are both photography and play but not
work?  What can do I when switching between them?

`git soc` is going to be the answer.

## Usage available today:

    # cd ~/src/
    # git clone https://github.com/hardaker/git-soc.git
    # cd git-soc
	# git soc register github/git-soc
    -- registering ~/lib/git-soc.d/work/github.yml
    
    # cd ~/lib/org
	# git soc register personal/org
    -- registering ~/lib/git-soc.d/personal/org.yml
    
    # cd ~
    # git soc status
    /home/hardaker/lib/org                                        
    /home/hardaker/src/git-soc                                   d (= dirty)

    # git soc push
    /home/hardaker/src/git-soc                                   fae63ca..0bb41cb
    /home/hardaker/lib/org                                       [up to date]

    # git soc pull
    /home/hardaker/lib/org                                       pulled
    /home/hardaker/src/git-soc                                   won't: dirty

    # git soc pushpull
    ... the same as both the above two commands ...

    # git soc cmd "ls .git"
    running command: ls .git
    --- /home/hardaker/lib/org
    Run here:  (y)es [default], (n)o, (q)uit: y
    running 'ls .git' in /home/hardaker/lib/org
    branches	config	     FETCH_HEAD  hooks	info  MERGE_RR	ORIG_HEAD    refs
    COMMIT_EDITMSG	description  HEAD	 index	logs  objects	packed-refs  rr-cache
    --- /home/hardaker/src/git-soc
    Run here:  (y)es [default], (n)o, (q)uit: y
    running 'ls .git' in /home/hardaker/src/git-soc
    branches	    COMMIT_EDITMSG.~2~	 config       HEAD   info      objects	    refs
    COMMIT_EDITMSG	    COMMIT_EDITMSG.~30~  description  hooks  logs      ORIG_HEAD    rr-cache
    COMMIT_EDITMSG.~1~  COMMIT_EDITMSG.~31~  FETCH_HEAD   index  MERGE_RR  packed-refs

## Usage to be done

- sync

    # git soc sync
    ... [interactive commit/add/push/pull] ...

- annex support

## (Eventual) Features

* Easy registration of new repos
* Supports `git annex` for large files
* Interactive (none of the other available options listed below are)
* Config files for repos in individual files
  * (easier to sync portions of repo sets around, rather than one
  monolithic config file)
* Easy configuration (automatic but editing yaml is possible if needed)
* Support for bootstrapping with ansible
* ideally multiple-commands at once in the background, stopping for
  interative when needed on some repos
* Startup from just a set of yaml files retrieved from another system 
  (after a new yaml files are found, it should auto-clone everything needed)

# Why not others

Right now a number of other projects exist to manage a large
collection of git repos, but they all don't quite match what I needed,
so I'm starting a new one.

* [antlink](https://ant.isi.edu/software/antlink/) - great for
managing a single tree of a lot of repos, with support for partial
tree-branch checkouts (the default) and grafting of external gitrepos.
Still a single place for a tree root to exist (though you could
symlink in).  Doesn't support `git annex`.  We hope to support antlink
sub-trees within git-soc.  Antlink is somewhat similar to but
different than:

* [repo](https://source.android.com/source/using-repo.html) - the repo
  management tool for the android toolkit.  Again, a large-tree
  collection but with poor documentation.

* [myrepos](https://myrepos.branchable.com/)

* [gr](https://github.com/mixu/gr):

* [mu](https://fabioz.github.io/mu-repo/): if there was one I would
  emulate as much as possible, it's this one.  It's support for
  parallelism is something I want to copy.  But that has no interactive
  support and it's configuration isn't splittable.

* [gitsync](https://github.com/simonthum/git-sync): I used this for a
  while and it supports a good registration mechanism, but is entirely
  automatic and doesn't support annex.

# other good reading

* [how to manage a large number of git repos](https://www.quora.com/Is-there-an-easy-way-to-manage-a-lot-of-git-repositories)
