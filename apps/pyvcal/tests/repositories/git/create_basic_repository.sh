mkdir testrepo01
cd testrepo01/

git init # note not init-bare

# add initial commit with empty README.txt
touch README.txt
git add README.txt
git commit -m "initial commit"

# put something into README.txt
echo "Hello world" > README.txt
git add README.txt # note even modified files must be added; can be skipped by doing a git commit -a but we'll do things the long way here
git commit -m "Edited README.txt"

# rename README.txt to README
git mv README.txt README # renamed files do not need to be git add'ed
git commit -m "Rename README.txt to README"

# delete README
git rm README
git commit -m "Delete README"


cd ../ # back out of testrepo01
