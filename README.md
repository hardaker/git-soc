# Design Goal

I wanted a tool to help manage logging into lots of systems with lots
of files and tools that need to be in lots of places.  But some
systems are for work, others for play, others for photography, etc.
And a different collection of files are needed on each system.  How
can I manage some systems that are both photography and play but not
work?  What can do I when switching between them?

`git soc` is going to be the answer.

## Features

- multi-processing for speed of operating on multiple repositories at once
- configuration for each registration stored as editable yaml

## Status

Works!  But I'm in the process of rewriting lots of it because, well,
let's just say I didn't know python very well when I started the
project.

# Install

    pip install git-soc

# Usage examples:

## Cloning a repo and then registering it

    # cd ~/src/
    # git clone https://github.com/hardaker/git-soc.git
    # cd git-soc
	# git soc register github/git-soc
    -- registering ~/lib/git-soc.d/work/github.yml
    
## Registering a second repository

    # cd ~/lib/org
	# git soc register personal/org
    -- registering ~/lib/git-soc.d/personal/org.yml

## Checking the status of all registered repositories
    
    # cd ~
    # git soc status
    /home/hardaker/lib/org                                        
    /home/hardaker/src/git-soc                                   d<>
                                                                 (d = dirty)
                                                                 (> = needs push)
                                                                 (< = needs merge)

## Running git push on every repository

    # git soc push
    /home/hardaker/src/git-soc                                   fae63ca..0bb41cb
    /home/hardaker/lib/org                                       [up to date]

## Running git fetch on every repository

    # git soc fetch
    /home/hardaker/lib/org                                       pulled
    /home/hardaker/src/git-soc                                   won't: dirty

## Running git pull on every repository

    # git soc pull
    /home/hardaker/lib/org                                       92e6422..831ba44
    /home/hardaker/src/git-soc                                   won't: dirty

## Running git push AND pull on every repository

    # git soc pushpull
    ... the same as both the above two commands ...

## Running an arbitrary command in each repository

    # git soc cmd "ls .git"
    --- /home/hardaker/lib/org
    running 'ls .git' in /home/hardaker/lib/org
    branches	config	     FETCH_HEAD  hooks	info  MERGE_RR	ORIG_HEAD    refs
    COMMIT_EDITMSG	description  HEAD	 index	logs  objects	packed-refs  rr-cache
    --- /home/hardaker/src/git-soc
    running 'ls .git' in /home/hardaker/src/git-soc
    branches	    COMMIT_EDITMSG.~2~	 config       HEAD   info      objects	    refs
    COMMIT_EDITMSG	    COMMIT_EDITMSG.~30~  description  hooks  logs      ORIG_HEAD    rr-cache
    COMMIT_EDITMSG.~1~  COMMIT_EDITMSG.~31~  FETCH_HEAD   index  MERGE_RR  packed-refs

# Repository configuration 

## Registration flags:

These registration flags are supported today:

### auto_commit:  true/false  (default = false)

Auto-commits any outstanding chasges; useful constantly saved
settings, files, emacs org files, etc.

### clone: true/false (default: true)

Whether or not to clone a repository if it doesn't exist.  By default,
things are cloned but a repo YAML file may set "clone: false" to
disable it from being pulled if it doesn't exist. 

## Usage to be done

- auto discover new commands
- add known files
- git annex support
- register with other arguments
  - auto_add

## (Eventual) Features

* Supports `git annex` for large files
* Easy configuration (automatic but editing yaml is possible if needed)
* Support for bootstrapping with ansible
* Startup from just a set of yaml files retrieved from another system 
  (after a new yaml files are found, it should auto-clone everything needed)

# Why not other tools

Right now a number of other projects exist to manage a large
collection of git repos, but they all don't quite match what I needed,
so I'm starting a new one.

* [antlink](https://ant.isi.edu/software/antlink/) - great for
managing a single tree of a lot of repos, with support for partial
tree-branch checkouts (the default) and grafting of external gitrepos.
Still a single place for a tree root to exist (though you could
symlink in).  Doesn't support `git annex`.  We hope to support antlink
sub-trees within git-soc.

* [repo](https://source.android.com/source/using-repo.html) - the repo
  management tool for the android toolkit.  Again, a large-tree
  collection but with poor documentation.

* [myrepos](https://myrepos.branchable.com/)

* [gr](https://github.com/mixu/gr):

* [mu](https://fabioz.github.io/mu-repo/): if there was one I would
  emulate as much as possible, it's this one.  But that has no
  interactive support and it's configuration isn't splittable.

* [gitsync](https://github.com/simonthum/git-sync): I used this for a
  while and it supports a good registration mechanism, but is entirely
  automatic and doesn't support annex.

# other good reading

* [how to manage a large number of git repos](https://www.quora.com/Is-there-an-easy-way-to-manage-a-lot-of-git-repositories)
