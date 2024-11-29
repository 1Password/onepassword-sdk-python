# change working directory to the directory of the script

cd "$(dirname "$0")"

# Run all python files in the tests directory
for file in *.py
do
	python3 $file
done