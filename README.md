# Incomplete project!!!

**NOTE:** This project is a template.  Not for public use yet, but will be
soon.  Drop me a line or an issue if it looks interesting and I'll
speed up where I can.

The files here are the hacking bash-wrapping versions that got me
thinking about the large project yet to come.

# Goal

I want a tool to help me manage logging into lots of machines with
lots of files that need to be in lots of places.  But some machines
are for work, others for play, others for photography, etc.  And a
different collection of files are needed on each machine.  How can I
manage some machines that are both photography and play but not work?
What can do I when switching between them?

`git soc` is going to be the answer.  Proposed usage:

    # cd ~/somewhere
	# git soc register work/somewhere
    -- registering ~/lib/git-soc/work/somewhere.yml
    
    # cd ~/lib/org
	# git soc register personal/org
    -- registering ~/lib/git-soc/personal/org.yml
    
    # git soc
    -- starting repo ~/lib/somewhere using work/somewhere.yml
    -- settings: autocommit, autoadd, annexlarge, interactive, autopush
    10 new files found, 3 changes, 1 deletion.
    (c)ommit-only, (a)dd and commit, (s)kip? c
	... git stuff happens ...
    ... auto push to main repo ...

(the above concept is significantly subject to change)

## Features

* Easy registration of new repos
* Supports `git annex` for large files
* Interactive (none of the options below are)
* Config files for repos in individual files
  * (easier to sync portions of repo sets around, rather than one
  monolithic file)
* Easy configuration (automatic but yaml if needed)
* Support for bootstrapping with ansible

# Why not others

Right now a number of other projects exist to manage a large
collection of git repos, but they all don't quite match what I needed,
so I'm starting a new one.

* [antlink](https://ant.isi.edu/software/antlink/) - great for
managing a single tree of a lot of repos.  Similar to:

* [repo](https://source.android.com/source/using-repo.html) - the repo
  management tool for the android toolkit.  Again, a large-tree
  collection but with poor documentation.

* [gitsync](https://github.com/simonthum/git-sync): I used this for a
  while and it supports a good registration mechanism, but is entirely
  automatic and doesn't support annex.
