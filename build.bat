echo ! Has README.rst been updated? !
pause
python setup.py sdist bdist_wheel
echo -----------------------------
echo Press ENTER to upload to PyPi
echo -----------------------------
pause
twine upload dist/*