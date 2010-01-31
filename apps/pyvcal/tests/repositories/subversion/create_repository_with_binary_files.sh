original_dir=$(pwd)
reponame="svn-with-binary-files"

mkdir $reponame
cd $reponame

# Creating a repository in this location
svnadmin create . 

svn_path=`pwd`

cd ../
mkdir repo02
cd repo02/

# Checking out the repository
svn co file://$svn_path

# Going into the repo dir
cd $reponame

# Copying some binary files into our repo
cp $original_dir/test-image.png .
cp $original_dir/test-image.png test-image
cat test-image.png | rev > blob

# Adding the files to our repo
svn add test-image.png test-image blob
svn ci -m "initial commit -> adding the files to the repo " test-image test-image.png blob

cd ../..


