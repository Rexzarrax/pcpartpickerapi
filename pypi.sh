# Build everything needed and upload to PyPi using twine

# https://cloudconvert.com/md-to-rst
echo Has README.rst been updated?
read -rsp $'Press enter to continue...\n'

echo Building /dist
rm -rf build dist
python setup.py sdist bdist_wheel

read -rsp $'Press enter to upload to PyPi...\n'
echo Uploading dist/* through twine
twine upload dist/*
