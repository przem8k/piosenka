# Piosenka z tekstem

[![Build Status](https://travis-ci.org/ppiet/piosenka.svg?branch=master)](https://travis-ci.org/ppiet/piosenka)

This web application powers a website dedicated to Polish singer-songwriters
hosted at https://www.piosenkaztekstem.pl.

## Get the code

```
git clone https://github.com/ppiet/piosenka.git
```

## Set up development environment

```
virtualenv -p `which python3.7` .virtualenv
source .virtualenv/bin/activate
pip install -r requirements.txt
```

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
