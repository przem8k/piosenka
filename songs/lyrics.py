""" Parsing and rendering of song lyrics. """
from django.template import Context, loader

from songs.transpose import transpose_lyrics


class LyricsParserMode:
    Regular = 0
    Recording = 1
    Replaying = 2


def parse_lyrics(raw_lyrics):
    """
    returns parsed lyrics as a list of paragraphs, each paragraph represented as a lists of tuples
    representing lines, each line as (text, chords, is_indented, are_chords_replayed)
    """
    result = []
    mode = LyricsParserMode.Regular
    recorded_section = None
    recorded_chords = []
    recordings = {}
    replayed_chords = []
    replay_index = -1
    current_section = []
    for raw_line in raw_lyrics.split('\n'):
        line = raw_line.strip()

        # Sanity checks.
        if line.find('{') != -1:
            raise SyntaxError(
                "'{}' brackets are the old way of specifying repeated chords. "
                "use section tags ('#zw', '@zw') instead.)")

        if len(line) == 0:
            # Empty line - finish current section.
            if recorded_section is not None:
                recordings[recorded_section] = recorded_chords
                recorded_section = None
                mode = LyricsParserMode.Regular
            if len(current_section) > 0:
                result.append(current_section)
                current_section = []
        elif line.startswith('#'):
            # Start new recording.
            if len(line) == 1:
                raise SyntaxError(
                    "Section defining tag (for example '#zw') can't have empty name.")
            recorded_section = line[1:]
            recorded_chords = []
            mode = LyricsParserMode.Recording
        elif line.startswith('@'):
            # Start replaying.
            if len(line) == 1:
                raise SyntaxError(
                    "Section reference tag (for example '@zw') can't have empty "
                    'name.')
            if not line[1:] in recordings:
                raise SyntaxError(
                    "Section had to be defined (with '#tag') before it can be "
                    "referenced (with '@tag').")
            replayed_chords = recordings[line[1:]]
            replay_index = 0
            mode = LyricsParserMode.Replaying
        else:
            # Regular line.
            textPart = ''
            chordsPart = ''
            if line.find('[') != -1:
                chordsStart = line.find('[')
                textPart = line[0:chordsStart].strip()
                chordsPart = line[chordsStart + 1:len(line) - 1].strip()
            else:
                textPart = line

            indent = False
            if textPart.startswith('>'):
                indent = True
                textPart = textPart[1:]

            are_chords_replayed = False
            if mode == LyricsParserMode.Recording:
                recorded_chords.append(chordsPart)
            elif mode == LyricsParserMode.Replaying:
                if replay_index < len(replayed_chords) and len(chordsPart) == 0:
                    chordsPart = replayed_chords[replay_index]
                    are_chords_replayed = True
                replay_index = replay_index + 1

            current_section.append(
                (textPart, chordsPart, indent, are_chords_replayed))
    if recorded_section is not None:
        recordings[recorded_section] = recorded_chords
        recorded_section = None
    if len(current_section) > 0:
        result.append(current_section)
    return result


def contain_extra_chords(raw_lyrics):
    for paragraph in raw_lyrics:
        for text, chords, is_indented, are_chords_extra in paragraph:
            if are_chords_extra:
                return True
    return False


def render_lyrics(raw_lyrics,
                  transposition=0,
                  template_name='songs/lyrics.html'):
    lyrics = transpose_lyrics(parse_lyrics(raw_lyrics), transposition)
    return loader.get_template(template_name).render(Context({'lyrics': lyrics
                                                             }))
