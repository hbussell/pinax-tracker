reponame="branch-and-merge"

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

file="fruit.txt"
echo "apple" > $file
echo "banana" >> $file
echo "cherry" >> $file
p4 -p 1666 add $file
p4 -p 1666 submit -d "Initial commit."

branch="branch"

p4 -p 1666 integ //depot/$trunk/... //depot/$branch/...
p4 -p 1666 edit ../$branch/$file
echo "date" >> ../$branch/$file
p4 -p 1666 submit -d "Big branch."

p4 -p 1666 edit $file 
echo "apples" > $file #erase previous contents of file
echo "bananas" >> $file
echo "cherry" >> $file
p4 -p 1666 submit -d "Pluralize fruit."

p4 -p 1666 integ //depot/$branch/... //depot/$trunk/...
p4 -p 1666 resolve -am
p4 -p 1666 submit -d "Merge."

cd ..

killall -SIGINT p4d

cd ../..


