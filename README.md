# Piosenka z tekstem

[![Build Status](https://travis-ci.org/ppiet/piosenka.svg?branch=master)](https://travis-ci.org/ppiet/piosenka)

This web application hosts https://www.piosenkaztekstem.pl .

## Get the code

```
git clone https://github.com/ppiet/piosenka.git
```

## Set up development environment

The current version uses Python3.9

Install Python and virtualenv (Mac instructions):

```
brew install python@3.9
```

```
pip3.9 install virtualenv
```

Initialize a virtualenv environment:

```
virtualenv -p `which python3.9` .virtualenv
source .virtualenv/bin/activate
pip install -r requirements.txt
```

May need to install postgresql as well:

```
brew install postgresql
```

## Run locally

```
python manage.py runserver
```

Then visit `http://localhost:8000/`

## Deploy

**Configuration**. Need to add/configure the following files with credentials:

 - private_gae_env.yaml
 - proxy_manage_py.sh – as described in the article [here](https://pnote.eu/notes/django-app-engine-guide/#schema-migrations)
 
**Check locally**. You can use the setup described @ https://cloud.google.com/python/django/appengine#connect_sql_locally to run a local instance
of the app against the real production database, to make sure the changes work as intended.

**Deploy**. You can deploy a new version using the script:
 
```
./deploy.sh
```

**Learn more**. The following articles describe the hosting setup of PzT on GCP:

 - https://pnote.eu/notes/django-app-engine-guide/
 - https://pnote.eu/notes/django-app-engine-user-uploaded-files/
 - https://pnote.eu/notes/django-app-engine-sending-email/
 - https://pnote.eu/notes/django-app-engine-cost/

## Contributing

Format source code using this script before sending a pull request:

```
./fix.sh
```
