#!/usr/bin/env bash

# Releases nisaba to pypi via specified tag

git tag $1 -m "$1"
git push --tags origin master
sed -i "s/x.x.x/$1/" setup.py # more files to add here if needed
python setup.py sdist
twine upload dist/*
sleep(5)
sudo pip install nisaba --upgrade
sed -i "s/$1/x.x.x/" setup.py # id id id
