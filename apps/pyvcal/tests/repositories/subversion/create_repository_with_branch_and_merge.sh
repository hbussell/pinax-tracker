reponame="svn-merge-branch"

mkdir $reponame
cd $reponame

# Creating a repository in this location
svnadmin create . 

svn_path=`pwd`

cd ../
mkdir repo05
cd repo05/

# Checking out the repository
svn co file://$svn_path

# Going into the repo dir
cd $reponame

# Making directories branches/ trunk/ and tags/
mkdir branches/
mkdir tags/
mkdir trunk/

# Adding and commiting the newly created dirs into this repository
svn add branches/ tags/ trunk/
svn ci -m "Adding the new repo structure to the repo" branches/ tags/ trunk/

# add initial commit with empty fruit.txt in the trunk
cd trunk/

touch fruit.txt
echo apple >fruit.txt 
echo banana >> fruit.txt  
echo cherry >> fruit.txt 

svn add fruit.txt
svn ci -m "initial commit of fruit into trunk " fruit.txt

cd ../

# Copying the elements of trunk into branches
svn copy trunk/ branches/my-branch
svn ci -m "commiting after copying trunk into branch"

cd branches/my-branch
echo date >> fruit.txt 

# Commiting my changes from branch 
svn ci -m "commit of fruit into branches " fruit.txt

# In trunk/ modify fruit.txt
cd ../../trunk/
echo apples >fruit.txt 
echo bananas >> fruit.txt  
echo cherry >> fruit.txt 
svn ci -m "Edited fruit.txt" fruit.txt

# Merge branch into trunk 
cd ../
# TODO: fix... this gives a conflict
svn merge -r 3:5 branches/my-branch/fruit.txt trunk/fruit.txt


cd ../ # back out of repo05

