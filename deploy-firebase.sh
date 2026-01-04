#!/bin/bash
set -e

python manage.py test
./build.sh
firebase deploy
