# Piosenka z tekstem

[![Build Status](https://travis-ci.org/ppiet/piosenka.svg?branch=master)](https://travis-ci.org/ppiet/piosenka)

This web application powers a website dedicated to Polish singer-songwriters
hosted at https://www.piosenkaztekstem.pl.

## Get the code

```
git clone https://github.com/ppiet/piosenka.git
```

## Set up development environment

The current version uses Python3.9.

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

(may need to comment out the last part of requirements.txt which is only needed on the server)

## Run locally

```
python manage.py runserver
```

Then visit `http://localhost:8000/`


## Format source code

```
./fix.sh
```

## Deploy

```
./deploy.sh
```

## Learn more

These articles describe the hosting setting of PzT on GCP App Engine:

 - https://pnote.eu/notes/django-app-engine-guide/
 - https://pnote.eu/notes/django-app-engine-user-uploaded-files/
 - https://pnote.eu/notes/django-app-engine-sending-email/
 - https://pnote.eu/notes/django-app-engine-cost/
