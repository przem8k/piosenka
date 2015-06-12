#!/bin/bash
set -e
coverage3 run --source='.' --omit='*migrations*,*commands*' manage.py test && coverage3 report
