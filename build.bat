pandoc --from=markdown --to=rst --output=README.rst README.md
python setup.py sdist bdist_wheel
echo -----------------------------
echo Press ENTER to upload to PyPi
echo -----------------------------
pause
twine upload dist/*