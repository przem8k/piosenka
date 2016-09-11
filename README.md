# Piosenka z tekstem #

[![Build Status](https://travis-ci.org/ppiet/piosenka.svg?branch=master)](https://travis-ci.org/ppiet/piosenka)

## Local dev setup ##

Install python requirements by running:

> pip install -r requirements.txt

## Restoring from backup ##

To restore the upload directory:

> aws s3 cp s3://BUCKET/upload/ upload --recursive

To restore the db:

> pg_restore -Ft --no-owner --username=USER --dbname=DB BACKUP.tar
