# Piosenka z tekstem

[![Build Status](https://travis-ci.org/ppiet/piosenka.svg?branch=master)](https://travis-ci.org/ppiet/piosenka)

**This web application powers a website dedicated to Polish singer-songwriters
hosted at https://www.piosenkaztekstem.pl. We have no ambition of generalizing
the code to power any other website or to support internationalized, ie.
non-Polish UI. Hence app strings and the rest of the documentation is in
Polish.**

## Konfiguracja środowiska

Piosenka z tekstem jest napisana w języku programowania Python. Aby uruchomić
aplikację należy zainstalować moduły wykorzystywane przez aplikację:

> pip3 install -r requirements.txt

Następnie można uruchomić aplikację lokalnie:

> python3 manage runserver

## Przygotowanie zmian

Przed wysłaniem zmian kodu strony warto sprawdzić, czy testy aplikacji nadal
działają:

> python3 manage test

## Administracja serwerem

Aby przywrócić pliki załadowane przez użytkowników aplikacji (np. nuty,
ilustracje do adnotacji).

> aws s3 cp s3://BUCKET/upload/ upload --recursive

Aby przywrócić zawartość bazy danych:

> pg_restore -Ft --no-owner --username=USER --dbname=DB BACKUP.tar
