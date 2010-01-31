reponame="empty-with-prop"

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

# TODO Set a property of some kind.

killall -SIGINT p4d

cd ../..


