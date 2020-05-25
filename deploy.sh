#!/bin/bash
set -e
if [[ -n $(git status --porcelain) ]]; then
    echo "Repo is dirty, aborting."
    exit 1
fi

rm -rf static
python manage.py collectstatic --noinput
python manage.py compress --force
gcloud app deploy
