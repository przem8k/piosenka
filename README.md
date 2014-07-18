# Piosenka z tekstem #

[![Build Status](https://drone.io/github.com/pietrzkiewicz/piosenka/status.png)](https://drone.io/github.com/pietrzkiewicz/piosenka/latest)

## Local dev setup ##

Install python requirements by running:

> pip install -r requirements.txt

Install node dependencies by running:

> npm install

## Restoring from backup ##

To restore the upload directory:

> aws s3 cp s3://BUCKET/upload/ upload --recursive

To restore the db:

> pg_restore -Ft --no-owner --username=USER --dbname=DB BACKUP.tar
