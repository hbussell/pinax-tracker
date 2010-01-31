reponame="with-dir"

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

mkdir dir
cd dir

touch file
p4 -p 1666 add file
p4 -p 1666 submit -d "Initial commit."

cd ..

killall -SIGINT p4d

cd ../..


