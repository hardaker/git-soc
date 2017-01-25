#!/bin/bash

src=`pwd`
dir=$src/git-soc-test
base="$dir/git-soc-base"

counter=1

cmd() {
    echo "=== $@"
    "$@"
}

cleanandinit() {
    # clean up and init
    cmd rm -rf $dir
    cmd mkdir -p $base
}

mkrepo() {
    name="$1"
    mkdir -p $dir/$name
    pushd $dir/$name
    git init --bare
    popd
}

clonerepo() {
    repo="$1"
    subdir="$2"
    pushd $dir
    git clone $1 $2
    popd
}

registerrepo() {
    repo="$1"
    pushd $dir/$repo
    gitsoc register $repo
    popd
}

title() {
    echo ""
    echo "========== $@"
}

gitsoc() {
    cmd $src/git-soc "$@" -B $base
}

mkmod() {
    repo="$1"
    pushd $dir/$repo
    echo $counter > counter
    git add counter
    git commit -m "counter $counter" counter
    counter=$(($counter + 1))
    popd
}   

cleanandinit

title" making repos"
mkrepo repo1
mkrepo repo2

title "cloning repos"
clonerepo repo1 repo1.w1
clonerepo repo1 repo1.w2
clonerepo repo2 repo2.w1
clonerepo repo2 repo2.w2

title "git-soc register"
registerrepo repo1.w1
registerrepo repo2.w1
registerrepo repo1.w2
registerrepo repo2.w2

title "status"
gitsoc status

title "make modifications"
mkmod repo1.w1
mkmod repo2.w1

title "status"
gitsoc status

title "push"
gitsoc push

title "pp"
gitsoc pull

title "push"
gitsoc push
