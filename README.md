# Piosenka z tekstem

Kod źródłowy i zawartość strony internetowej [piosenkaztekstem.pl](https://www.piosenkaztekstem.pl).

Zawartość strony znajduje się w plikach Markdown w folderze [pages](pages). Przykładowo, treść piosenki 1788 znajduje się w pliku [pages/opracowanie/jacek-kaczmarski-1788/index.md](https://raw.githubusercontent.com/przem8k/piosenka/refs/heads/main/pages/opracowanie/jacek-kaczmarski-1788/index.md). Adnotacja do piosenki znajduje się w umieszczonym obok pliku [pages/opracowanie/jacek-kaczmarski-1788/rok-1788.md](https://raw.githubusercontent.com/przem8k/piosenka/refs/heads/main/pages/opracowanie/jacek-kaczmarski-1788/rok-1788.md)

Szablony HTML znajdują się w folderze [templates](templates).

Pliki strony w formacie gotowym do publikacji są generowane na podstawie plików Markdown i szablonów przy pomocy programu [gen.py](piosenka/management/commands/gen.py).

Pomocniczy skrypt [build.sh](build.sh) pozwala wygenerować stronę jedną komendą.

Zapraszamy do nadsyłania poprawek w formie pull requestów!