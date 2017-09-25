# Client

Ten katalog zawiera arkusze styli i kod JavaScript wykonywany w przeglądarce
użytkownika (*client-side*).

Kompilacją plików w tym katalogu zarządza narzędzie Webpack, skonfigurowane wg.
opisu (za wyjątkiem fragmentów dotyczących komponentów React):

 - http://owaislone.org/blog/webpack-plus-reactjs-and-django/

W czasie pracy nad kodem w tym katalogu, należy pozostawić uruchomione polecenie:

```
cd client
./node_modules/.bin/webpack --config webpack.config.js --watch
```

Wcześniej należy zainstalować pakiety NodeJS wymagane przez PzT:

```
cd client
npm install
```
