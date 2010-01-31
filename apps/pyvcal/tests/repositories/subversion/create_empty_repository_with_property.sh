reponame="svn-empty-with-prop"

mkdir $reponame
cd $reponame

# Creating a repository in this location
svnadmin create . 

svn_path=`pwd`

cd ../
mkdir repo04
cd repo04/

# Checking out the repository
svn co file://$svn_path

# Going into the repo dir
cd $reponame

# TODO Set a property of some kind.

cd ../..

