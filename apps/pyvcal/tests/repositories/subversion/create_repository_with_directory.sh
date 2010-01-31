reponame="svn-with-dir"

mkdir $reponame
cd $reponame

# Creating a repository in this location
svnadmin create . 

svn_path=`pwd`

cd ../
mkdir repo03
cd repo03/

# Checking out the repository
svn co file://$svn_path

# Going into the repo dir
cd $reponame

mkdir dir
# adding the new dir to the repository
svn add dir

cd dir
touch file
# Adding the newly created file to the repository
svn add file

cd ../
# Commiting the file and dir into the repository
svn ci -m "Initial commit --> file and new dir."

cd ..



