#!/bin/bash
set -e
if [[ -n $(git status --porcelain) ]]; then
    echo "Repo is dirty, aborting."
    exit 1
fi

python manage.py test
./build.sh
firebase deploy
