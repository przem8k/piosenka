#!/bin/bash
set -e
if [[ -n $(git status --porcelain) ]]; then
    echo "Repo is dirty, aborting."
    exit 1
fi

git pull
python3 manage.py migrate
python3 manage.py collectstatic --noinput
appctl restart piosenka
