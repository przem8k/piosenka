KEY_TO_ORD = {
    'c': 0,
    'cis': 1,
    'des': 1,
    'd': 2,
    'dis': 3,
    'e': 4,
    'es': 4,
    'f': 5,
    'fis': 6,
    'ges': 6,
    'g': 7,
    'gis': 8,
    'as': 8,
    'a': 9,
    'b': 10,
    'ais': 10,
    'h': 11
}

ORD_TO_KEY = {
    0: 'c',
    1: 'cis',
    2: 'd',
    3: 'dis',
    4: 'e',
    5: 'f',
    6: 'fis',
    7: 'g',
    8: 'gis',
    9: 'a',
    10: 'b',
    11: 'h'
}

# These chords cause trouble when parsing from the left side, eg. in Asus4 -> As us4.
KNOWN_CHORD_TYPES = {
    "sus4": "",
    "sus2": "",
}


def parse_chord(chord):
    """
    Parses a chord into a tuple of (root sound, chord type, base sound).

    >>> parse_chord('a')
    ('a', '', '')
    >>> parse_chord('A')
    ('A', '', '')
    >>> parse_chord('C7')
    ('C', '7', '')
    >>> parse_chord('Asus4/H')
    ('A', 'sus4', 'H')
    >>> parse_chord('Assus2/H')
    ('As', 'sus2', 'H')
    >>> parse_chord('Amaj7')
    ('A', 'maj7', '')
    >>> parse_chord('Esmaj7')
    ('Es', 'maj7', '')
    >>> parse_chord('Fismaj7')
    ('Fis', 'maj7', '')
    >>> parse_chord('h7/a')
    ('h', '7', 'a')
    >>> parse_chord('H/a')
    ('H', '', 'a')
    """
    if chord.find("/") != -1:  # for chords with specified base sound
        if chord.find("/") == 0 or chord.find("/") == len(chord) - 1 or chord.count("/") > 1:
            raise SyntaxError("/ is for base sounds, use it like this: D7/f, a/h (no spaces "
                              "before or after /).")
        base_sound = chord[chord.find("/") + 1:]
        rest = chord[:chord.find("/")]
    else:
        base_sound = ""
        rest = chord

    # First check for a known suffix (chord type) to handle chord types that yield bogus root sounds
    # (e.g. A + sus4 gives "As" at the beginning).
    for start in range(1, len(rest)):
        suf = rest[start:]
        if suf.lower() in KNOWN_CHORD_TYPES:
            return (rest[:start], suf, base_sound,)

    # Then check for a known prefix (base sound).
    for end in reversed(range(1, 4)):
        pref = rest[:end]
        if pref.lower() in KEY_TO_ORD:
            return (pref, rest[end:], base_sound,)

    raise SyntaxError("I can't recognize the chord: " + chord)


def transpose_sound(sound, transposition):
    """
    Transposes a sound a given number of semitones up or down.

    >>> transpose_sound('a', 0)
    'a'
    >>> transpose_sound('a', -2)
    'g'
    >>> transpose_sound('a', 1)
    'b'
    >>> transpose_sound('a', 3)
    'c'
    >>> transpose_sound('a', 12)
    'a'
    """
    normalized = sound.lower()
    if normalized not in KEY_TO_ORD:
        raise SyntaxError("I can't recognize '%s' as a valid sound." % (sound,))

    transposed = ORD_TO_KEY[(KEY_TO_ORD[normalized] + transposition) % 12]
    return transposed.capitalize() if sound[0].isupper() else transposed


def transpose_chord(chord, t):
    """
    Transposes a chord >without a base sound< a given number of halftones up
    """
    root_sound, chord_type, base_sound = parse_chord(chord)
    if base_sound:
        return transpose_sound(root_sound, t) + chord_type + "/" + transpose_sound(base_sound, t)
    else:
        return transpose_sound(root_sound, t) + chord_type


def transpose_sequence(chord_sequence, transposition):
    """
    Transposes a sequence of chords separated by whitespace a given number of halftones up. Chords
    with specified base sounds are split and the sound is transposed separately.

    >>> transpose_sequence('D G D/A A7 D', 2)
    'E A E/H H7 E'
    >>> transpose_sequence('c Gis0/C', 11)
    'h G0/H'
    """
    return ' '.join([transpose_chord(x, transposition) for x in chord_sequence.split()])


def transpose_lyrics(parsed_lyrics, transposition):
    """
    Transposes a song represented as a list of paragraphs and returns result in the same format
    >>> transpose_lyrics([[('Na ziemi.', 'a a/H a/C a/D (a/E a/F a/E a E4/H)', False, False)]], 2)
    [[('Na ziemi.', 'h h/Cis h/D h/E (h/Fis h/G h/Fis h Fis4/Cis)', False, False)]]
    >>> transpose_lyrics([[('Abc.', 'e a C H7 C H7 (e Fis0 E0 e C H7)', True, True)]], 5)
    [[('Abc.', 'a d F E7 F E7 (a H0 A0 a F E7)', True, True)]]
    """
    result = []
    for paragraph in parsed_lyrics:
        section = []
        for (text, chords, is_indented, are_chords_replayed) in paragraph:
            if chords.find("(") != -1:
                if (chords.count("(") != 1 or chords.count(")") != 1 or
                        chords.find(")") != len(chords) - 1) or chords.find("(") > chords.find(")"):
                    raise SyntaxError("I don't understand the line: '" + chords + "'. "
                                      "'(', ')' brackets should contain "
                                      "chords played without singing at the end of the verse, for "
                                      "example: 'a C (H7 C)'. Don't put anything after ')'.")
                left_bracket = chords.find("(")
                right_bracket = chords.find(")")
                core = chords[:left_bracket].strip()
                bracketed = chords[left_bracket + 1:right_bracket].strip()
                transposed = "%s (%s)" % (transpose_sequence(core, transposition),
                                          transpose_sequence(bracketed, transposition))
            else:
                transposed = transpose_sequence(chords, transposition)
            section.append((text, transposed, is_indented, are_chords_replayed,))
        result.append(section)
    return result
