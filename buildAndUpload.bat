:: Build everything needed and upload to PyPi using twine (recommended)
@echo off
echo ! Has README.rst been updated? !
pause
echo Building /dist
rm -rf build dist
python setup.py sdist bdist_wheel
echo -----------------------------
echo Press ENTER to upload to PyPi
echo -----------------------------
pause
echo Uploading dist/* through twine
twine upload dist/*