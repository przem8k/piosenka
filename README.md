# Piosenka z tekstem

[![Build Status](https://travis-ci.org/ppiet/piosenka.svg?branch=master)](https://travis-ci.org/ppiet/piosenka)

**This web application powers a website dedicated to Polish singer-songwriters
hosted at https://www.piosenkaztekstem.pl. We have no ambition of generalizing
the code to power any other website or to support internationalized, ie.
non-Polish UI. Hence app strings and the rest of the documentation is in
Polish.**

## Pozyskanie kodu źródłowego

Aplikacja jest "open source" i jej kod jest dostępny publicznie. Aby ściągnąć
kod aplikacji, upewnij się że na komputerze zainstalowany jest system
zarządzania kodem źródłowym `git`.

Następnie uruchom komendę:

> git clone https://github.com/ppiet/piosenka.git

## Konfiguracja środowiska

Piosenka z tekstem jest napisana w języku programowania Python. Aby uruchomić
aplikację należy zainstalować moduły wykorzystywane przez aplikację:

> pip3 install -r requirements.txt

Następnie można uruchomić aplikację lokalnie:

> python3 manage runserver

Lokalna wersja aplikacji jest dostępna w przeglądarce pod adresem
`http://127.0.0.1:8000`.

## Przygotowanie zmian

### JS / CSS

Zmiany obejmujące arkusze styli CSS oraz kod JavaScript (a więc te obejmujące
kod wykonywany w przeglądarce użytkownika) wymagają przetworzenia przez
narzędzie webpack.

```
cd client
./node_modules/.bin/webpack --config webpack.config.js
```

webpack generuje skonsolidawne i skompresowane pliki JS i CSS które łączą wiele
niezależnych zasobów w pojedynczy plik, zapewniając szybsze ładowanie strony.

### Testy

Przed wysłaniem zmian kodu strony warto sprawdzić, czy testy aplikacji nadal
działają:

> python3 manage test

## Administracja serwerem

Aby przywrócić pliki załadowane przez użytkowników aplikacji (np. nuty,
ilustracje do adnotacji).

> aws s3 cp s3://BUCKET/upload/ upload --recursive

Aby przywrócić zawartość bazy danych:

> pg_restore -Ft --no-owner --username=USER --dbname=DB BACKUP.tar
