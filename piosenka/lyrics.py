""" Parsing and rendering of song lyrics. """

import re

from django.template import Context, loader
from django.utils.html import escape
from django.utils.safestring import mark_safe

from piosenka.transpose import transpose_lyrics

MARK = "^"


class LyricsParserMode:
    Regular = 0
    Recording = 1
    Replaying = 2


def split_chords(chords):
    """
    Splits chords into the sung ones and the group in parentheses.

    >>> split_chords('a C (E7)')
    (['a', 'C'], '(E7)')
    >>> split_chords('( a )')
    ([], '( a )')
    """
    idx = chords.find("(")
    if idx == -1:
        return chords.split(), ""
    return chords[:idx].split(), chords[idx:].strip()


def mark_text(text, chords):
    """
    Returns the text as HTML with an empty chord mark in place of ^ (one mark for ^^). song.js fills
    in the chords. A tail mark is added for chords after the text: the group in parentheses, or all
    chords if there is no text.

    >>> print(mark_text('Sku^lony w <b>jakiejś</b>', 'a'))
    Sku<span class="ch"></span>lony w &lt;b&gt;jakiejś&lt;/b&gt;
    >>> print(mark_text('I ^^spały', 'F E (a)'))
    I <span class="ch" data-n="2"></span>spały<span class="ch tail"></span>
    >>> print(mark_text('', 'a C'))
    <span class="ch tail"></span>
    """

    def mark(match):
        n = len(match.group())
        return '<span class="ch"%s></span>' % (f' data-n="{n}"' if n > 1 else "")

    html = re.sub(r"\^+", mark, escape(text))
    _, tail = split_chords(chords)
    if tail or (chords and not text.strip()):
        html += '<span class="ch tail"></span>'
    return mark_safe(html)


def build_lines(sections, slug):
    """
    Checks the ^ marks and turns (text, chords, is_indented, line_no) into (text, chords,
    is_indented). Wrong number of marks is an error. Chords above the text only if all lines with
    text and chords have marks, otherwise classic view and a warning. line_no counts from the start
    of the lyrics. Returns (paragraphs, positioned).
    """
    has_marks = False
    missing = []
    errors = []
    for paragraph in sections:
        for text, chords, _, line_no in paragraph:
            marks = text.count(MARK)
            sung, _ = split_chords(chords)
            if marks and marks != len(sung):
                errors.append(
                    f"  line {line_no}: {marks} marks but {len(sung)} chords "
                    f"({' '.join(sung)}): {text!r}"
                )
            if marks:
                has_marks = True
            elif sung and text.strip():
                missing.append(line_no)
    if errors:
        raise SyntaxError("wrong number of '^' marks:\n" + "\n".join(errors))
    positioned = has_marks and not missing
    if has_marks and missing:
        print(
            f"WARNING {slug}: chord position marks ('^') are missing in lines "
            f"{missing}, showing the classic view only"
        )

    result = []
    for paragraph in sections:
        lines = []
        for text, chords, indent, _ in paragraph:
            if positioned:
                text = mark_text(text, chords)
            else:
                text = text.replace(MARK, "")
            lines.append((text, chords, indent))
        result.append(lines)
    return result, positioned


def parse_lyrics(raw_lyrics, slug=""):
    r"""
    returns (paragraphs, has_positions). Each paragraph is a list of (text, chords, is_indented)
    lines. With has_positions, text is HTML with chord marks.

    >>> parse_lyrics("I ^spały małe [F]\nŁeb podniósł [F]", "test")
    WARNING test: chord position marks ('^') are missing in lines [2], showing the classic view only
    ([[('I spały małe', 'F', False), ('Łeb podniósł', 'F', False)]], False)
    >>> parse_lyrics("Sku^lony w jakiejś ^ciemnej [a C G]\nI ^spały [F]\nWtem ^stary ^wilk [a]")
    Traceback (most recent call last):
    SyntaxError: wrong number of '^' marks:
      line 1: 2 marks but 3 chords (a C G): 'Sku^lony w jakiejś ^ciemnej'
      line 3: 2 marks but 1 chords (a): 'Wtem ^stary ^wilk'
    """
    result = []
    mode = LyricsParserMode.Regular
    recorded_section = None
    recorded_chords = []
    recordings = {}
    replayed_chords = []
    replay_index = -1
    current_section = []
    for line_no, raw_line in enumerate(raw_lyrics.split("\n"), 1):
        line = raw_line.strip()

        # Sanity checks.
        if line.find("{") != -1:
            raise SyntaxError(
                "'{}' brackets are the old way of specifying repeated chords. "
                "use section tags ('#zw', '@zw') instead.)"
            )

        if len(line) == 0:
            # Empty line - finish current section.
            if recorded_section is not None:
                recordings[recorded_section] = recorded_chords
                recorded_section = None
                mode = LyricsParserMode.Regular
            if len(current_section) > 0:
                result.append(current_section)
                current_section = []
        elif line.startswith("#"):
            # Start new recording.
            if len(line) == 1:
                raise SyntaxError(
                    "Section defining tag (for example '#zw') can't have empty name."
                )
            recorded_section = line[1:]
            recorded_chords = []
            mode = LyricsParserMode.Recording
        elif line.startswith("@"):
            # Start replaying.
            if len(line) == 1:
                raise SyntaxError(
                    "Section reference tag (for example '@zw') can't have empty "
                    "name."
                )
            if not line[1:] in recordings:
                raise SyntaxError(
                    "Section had to be defined (with '#tag') before it can be "
                    "referenced (with '@tag')."
                )
            replayed_chords = recordings[line[1:]]
            replay_index = 0
            mode = LyricsParserMode.Replaying
        else:
            # Regular line.
            textPart = ""
            chordsPart = ""
            if line.find("[") != -1:
                chordsStart = line.find("[")
                textPart = line[0:chordsStart].strip()
                chordsPart = line[chordsStart + 1 : len(line) - 1].strip()
            else:
                textPart = line

            # "^>" works the same as ">^"
            if textPart.startswith(MARK + ">"):
                textPart = ">" + MARK + textPart[2:]

            indent = False
            if textPart.startswith(">"):
                indent = True
                textPart = textPart[1:]

            if mode == LyricsParserMode.Recording:
                recorded_chords.append(chordsPart)
            elif mode == LyricsParserMode.Replaying:
                if replay_index < len(replayed_chords) and len(chordsPart) == 0:
                    chordsPart = replayed_chords[replay_index]
                replay_index = replay_index + 1

            current_section.append((textPart, chordsPart, indent, line_no))
    if recorded_section is not None:
        recordings[recorded_section] = recorded_chords
        recorded_section = None
    if len(current_section) > 0:
        result.append(current_section)
    return build_lines(result, slug)


def render_lyrics(raw_lyrics, slug="", template_name="songs/lyrics.html"):
    """
    Returns (html, has_positions).

    >>> '<td>I <span class="ch"></span>spały</td>' in render_lyrics("I ^spały [F]")[0]
    True
    """
    parsed, has_positions = parse_lyrics(raw_lyrics, slug)
    lyrics = transpose_lyrics(parsed)
    html = loader.get_template(template_name).render({"lyrics": lyrics})
    return html, has_positions
