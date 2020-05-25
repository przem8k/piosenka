#!/bin/bash
set -e

git ls-files | grep .py | grep -v migrations | grep -v manage.py | grep -v assets | xargs yapf -i

git ls-files | grep .py | grep -v migrations | grep -v manage.py | grep -v assets | xargs isort
