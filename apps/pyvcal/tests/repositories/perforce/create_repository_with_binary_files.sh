original_dir=$(pwd)
reponame="with-binary-files"

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

cp $original_dir/test-image.png .
cp $original_dir/test-image.png test-image
cat test-image.png | rev > blob

p4 -p 1666 add test-image.png
p4 -p 1666 add test-image
p4 -p 1666 add blob 

p4 -p 1666 submit -d "Initial commit."

killall -SIGINT p4d

cd ../..


