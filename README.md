# Piosenka z tekstem

Kod źródłowy i zawartość strony internetowej [piosenkaztekstem.pl](https://www.piosenkaztekstem.pl).

## Struktura repozytorium

Zawartość strony znajduje się w plikach Markdown w folderze [pages](pages). Przykładowo, treść piosenki 1788 znajduje się w pliku [pages/opracowanie/jacek-kaczmarski-1788/index.md](https://raw.githubusercontent.com/przem8k/piosenka/refs/heads/main/pages/opracowanie/jacek-kaczmarski-1788/index.md). Adnotacja do piosenki znajduje się w umieszczonym obok pliku [pages/opracowanie/jacek-kaczmarski-1788/rok-1788.md](https://raw.githubusercontent.com/przem8k/piosenka/refs/heads/main/pages/opracowanie/jacek-kaczmarski-1788/rok-1788.md)

Szablony HTML znajdują się w folderze [templates](templates).

Pliki strony w formacie gotowym do publikacji są generowane na podstawie plików Markdown i szablonów przy pomocy programu [gen.py](piosenka/management/commands/gen.py).

## Składnia opracowania piosenki

Opracowanie piosenki to plik `pages/opracowanie/<piosenka>/index.md`. Pod nagłówkiem (między liniami `---`) jest tekst z akordami, np. fragment „Obławy”:

```
#zw
Skulony w jakiejś ciemnej jamie smaczniem sobie spał [a C G C]
I spały małe wilczki dwa – zupełnie ślepe jeszcze [F E]

#ref
>Obława! Obława! Na młode wilki obława! [a C G C]
>Te dzikie, zapalczywe, w gęstym lesie wychowane! [F E]

@zw
Ten, który rzucił na mnie się, niewiele szczęścia miał,
Bo wypadł prosto mi na kły i krew trysnęła z rany
```

- Akordy wpisuje się w nawiasie kwadratowym na końcu linii: `[a C G C]`. Na stronie wyświetlają się po prawej stronie tekstu.
- Pusta linia kończy zwrotkę lub refren.
- `#nazwa` (np. `#ref`) oznacza zwrotkę, której akordy są wzorem dla kolejnych.
- `@nazwa` (np. `@ref`) oznacza kolejną zwrotkę z tymi samymi akordami. Akordów się w niej nie wpisuje, bo są przepisywane z `#nazwa` linia po linii. Jeśli któraś linia ma inne akordy, można je wpisać w niej normalnie w nawiasach kwadratowych, akordy z `#nazwa` zostaną nadpisane.
- Linia zaczynająca się od `>` jest wcięta (zwykle refren).
- W nawiasie okrągłym na końcu można zapisać akordy przejściowe, np. `[F E (a)]`; są to akordy grane już bez śpiewu, na końcu wersu.
- Można też podać linie z samymi akordami, bez tekstu, np. jako wstęp: `[a E a E]`.

### Akordy nad sylabami (opcjonalnie)

W opracowaniu można dodatkowo wskazać, na której sylabie wchodzi każdy akord. Wtedy na stronie pojawia się przycisk „akordy nad tekstem”, który wyświetla je nad sylabą zamiast po prawej.

W tym celu trzeba wstawić znak daszka: `^` bezpośrednio przed sylabą, na której wchodzi akord. Pierwszy `^` w linii dostaje pierwszy akord z podanych w nawiasie, drugi `^` dostaje drugi akord itd. W przypadku korzystania z `@nazwa` akordów nadal się nie wpisuje, ale trzeba wpisać znaczniki `^`:

```
#zw
Sku^lony w jakiejś ^ciemnej jamie ^smaczniem sobie ^spał [a C G C]
I ^spały małe wilczki dwa - zu^pełnie ślepe jeszcze [F E]

#ref
>O^bława! O^bława! Na ^młode wilki o^bława! [a C G C]
>Te ^dzikie, zapalczywe, w gęstym ^lesie wychowane! [F E]

@zw
Ten, ^który rzucił ^na mnie się, nie^wiele szczęścia ^miał
Bo ^wypadł prosto mi na kły i ^krew trysnęła z rany
```

- znacznik `^` może stać w środku słowa (`Sku^lony`), przed słowem (`^ciemnej`) albo po ostatnim słowie (`spał ^`), jeśli akord wchodzi po tekście. `^^` to dwa akordy obok siebie.
- W linii wciętej sugerowana kolejność zapisu to: `>^Te dzikie`.
- W przypadku akordów przejściowych (w nawiasie okrągłym) nie należy wstawiać znaczników `^`, te akordy wyświetlają się same na końcu linii. Linie z samymi akordami, np. `[a E]`, również nie potrzebują `^`.
- Liczba `^` w linii musi być równa liczbie akordów (poza akordami przejściowymi). Inaczej strona nie zbuduje się poprawnie, a komunikat wskaże niepoprawnie zapisaną piosenkę i problematyczne linie. Numer linii liczy się od początku tekstu piosenki, nie od początku pliku.
- `^` trzeba wstawić we wszystkich liniach z tekstem i akordami. Jeśli w części linii ich brakuje, generator wypisze ostrzeżenie, a piosenka będzie dostępna tylko w zwykłym widoku.
- Na stronie domyślny jest zwykły widok. Wybór trybu przeglądarka zapamiętuje w local storage. Jeżeli zostanie wybrany tryb „akordy nad tekstem”, a dana piosenka będzie miała w opracowaniu wstawione znaczniki, to będzie wyświetlał się ten tryb.

Zapraszamy do nadsyłania poprawek w formie pull requestów!

## Przydatne komendy

### Zarządzanie zależnościami (dependencies)

Projekt używa `uv` do zarządzania pomocniczymi bibliotekami potrzebnymi do wygenerwania strony. Aby je zainstalować i załadować:

1. Utwórz wirtualne środowisko:

```bash
uv venv
```

2. Aktywuj wirtualne środowisko:

```bash
source .venv/bin/activate
```

3. Zainstaluj zależności:

```bash
uv sync
```

### Generowanie strony i uruchamianie serwera

Pomocniczy skrypt [build.sh](build.sh) pozwala wygenerować stronę jedną komendą.

Aby zobaczyć wygenerowane lokalnie pliki z poprawnie ładującymi się stylami, warto uruchomić lokalny server:

```
python manage.py runserver
```

Po uruchomieniu serwera, lokalnie wygenerowana wersja strony jest dostępna pod adresem http://localhost:8000/

## Publikacja

Zawartość strony jest automatycznie generowana i publikowana do Firebase Hosting po każdej zmianie (push) w gałęzi `main` na GitHubie. Proces publikacji jest zdefiniowany w pliku [.github/workflows/publish.yaml](.github/workflows/publish.yaml)