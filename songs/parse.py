class LyricsParserMode:
    Regular = 0
    Recording = 1
    Replaying = 2


def parse_lyrics(raw_lyrics):
    """
    returns parsed lyrics as a list of paragraphs, each paragraph represented as a lists of tuples
    representing lines, each line as (text, chords, is_indented, are_chords_extra)
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

        # Finish current section.
        if len(line) == 0:
            if recorded_section is not None:
                recordings[recorded_section] = recorded_chords
                recorded_section = None
                mode = LyricsParserMode.Regular
            if len(current_section) > 0:
                result.append(current_section)
                current_section = []

        # Start new recording.
        if line.startswith('#'):
            if len(line) == 1:
                raise SyntaxError("Empty paragraph tag (#TAG) name")
            recorded_section = line[1:]
            recorded_chords = []
            mode = LyricsParserMode.Recording
        elif line.startswith('@'):
            if len(line) == 1:
                raise SyntaxError("Empty paragraph tag reference (@TAG) name")
            if not line[1:] in recordings:
                raise SyntaxError("Paragraph was referenced by @TAG before it was defined by #TAG")
            replayed_chords = recordings[line[1:]]
            replay_index = 0
            mode = LyricsParserMode.Replaying
        else:
            textPart = ""
            chordsPart = ""
            are_chords_extra = False
            if line.find("[") != -1:
                chordsStart = line.find("[")
                textPart = line[0:chordsStart]
                chordsPart = line[chordsStart+1:len(line)-1]
            elif line.find("{") != -1:
                chordsStart = line.find("{")
                textPart = line[0:chordsStart]
                chordsPart = line[chordsStart+1:len(line)-1]
                are_chords_extra = True
            else:
                textPart = line

            indent = False
            if textPart.startswith(">"):
                indent = True
                textPart = textPart[1:]

            if mode == LyricsParserMode.Recording:
                if are_chords_extra:
                    raise SyntaxError("Paragraph tagged for reference cannot contain repeated "
                                      "chords / chords in {} brackets")
                recorded_chords.append(chordsPart)
            elif mode == LyricsParserMode.Replaying:
                if replay_index < len(replayed_chords) and len(chordsPart) == 0:
                    chordsPart = replayed_chords[replay_index]
                    are_chords_extra = True
                replay_index = replay_index + 1

            current_section.append((textPart, chordsPart, indent, are_chords_extra))
    if recorded_section is not None:
        recordings[recorded_section] = recorded_chords
        recorded_section = None
    if len(current_section) > 0:
        result.append(current_section)
    return result
