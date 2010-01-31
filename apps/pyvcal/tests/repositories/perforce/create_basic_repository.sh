reponame="basic"

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

touch README.txt
p4 -p 1666 add README.txt 
p4 -p 1666 submit -d "initial commit"

p4 -p 1666 edit README.txt 
echo "Hello, world." > README.txt 
p4 -p 1666 submit -d "Edit README.txt"

p4 -p 1666 integrate README.txt README
p4 -p 1666 delete README.txt 
p4 -p 1666 submit -d "Rename README.txt to README"

p4 -p 1666 delete README 
p4 -p 1666 submit -d "Delete README"

killall -SIGINT p4d

cd ../..


