reponame="rebase"

mkdir $reponame
cd $reponame

mkdir repo
cd repo

p4d &
sleep 1 # Let p4d start.

cd ..
mkdir client
cd client

spec="clientspec"

# A pipe occasionally causes (threading?) errors
p4 -p 1666 client -o > $spec
p4 -p 1666 client -i < $spec
rm $spec

trunk="main"

mkdir $trunk
cd $trunk

file="file.txt"
touch $file
p4 -p 1666 add $file
p4 -p 1666 submit -d "Initial commit."

branch="branch"

p4 -p 1666 integ //depot/$trunk/... //depot/$branch/...
touch ../$branch/new.txt
p4 -p 1666 add ../$branch/new.txt
p4 -p 1666 submit -d "Add new file in branch."

p4 -p 1666 edit $file
echo "All your rebase" > $file
p4 -p 1666 submit -d "All your rebase"

p4 -p 1666 integ //depot/$trunk/... //depot/$branch/...
p4 -p 1666 resolve -am
p4 -p 1666 submit -d "Update branch from trunk."

p4 -p 1666 edit ../$branch/$file
echo " are belong to us" >> ../$branch/$file
p4 -p 1666 submit -d "All your branch are belong to us."

p4 -p 1666 integ //depot/$branch/... //depot/$trunk/...
p4 -p 1666 resolve -am
p4 -p 1666 submit -d "Merge."

cd ..

killall -SIGINT p4d

cd ../..


