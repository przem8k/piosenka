# piosenkaztekstem

This project contains a static site generator and the page content for a website
called "Piosenka z tekstem". 

## Historical context

This used to be a dynamic website running using Django. It was then converted
into a static page and now its content is managed using GitHub pull requests.
The generator that creates the output HTML from the content pages is still
implemented as a Django command in piosenka/management/commands/gen.py
and the templates are Django templates. This is for historical reasons, as it
made the transition easier.

## Languages

The website and developer-facing instructions in README.md are in Polish. The
code, code comments and git commit descriptions are in English.
