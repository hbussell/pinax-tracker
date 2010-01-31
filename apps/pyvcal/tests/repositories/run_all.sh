cd git
./create_basic_repository.sh

cd ../subversion
./create_basic_repository.sh

cd ../perforce
./create_basic_repository.sh
./create_empty_repository_with_property.sh
./create_repository_with_binary_files.sh
./create_repository_with_directory.sh
