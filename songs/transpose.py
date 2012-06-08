import string

KEYS_TO_ORD = {
    'c' : 0, 
    'cis': 1, 
    'des': 1, 
    'd': 2, 
    'dis' : 3, 
    'e' : 4, 
    'es' : 4, 
    'f': 5, 
    'fis': 6, 
    'ges': 6, 
    'g' : 7, 
    'gis': 8, 
    'as': 8, 
    'a': 9, 
    'b': 10, 
    'ais': 10, 
    'h' : 11
}

ORD_TO_KEY = {
    0 : 'c',
    1 : 'cis',
    2 : 'd',
    3 : 'dis',
    4 : 'e',
    5 : 'f',
    6 : 'fis',
    7 : 'g',
    8 : 'gis',
    9 : 'a',
    10 : 'b',
    11 : 'h'
}

def transpose_chord(chord, transposition):
    """ Transposes a chord >without a base sound< a given number of halftones up """
        low = chord[0].lower() + chord[1:]

        transposed = "??"
        for prefix_length in [3,2,1]:
            if len(low) >= prefix_length and low[:prefix_length] in KEYS_TO_ORD:
                new_ord = (KEYS_TO_ORD[low[:prefix_length]] + transposition) % 12
                transposed = ORD_TO_KEY[new_ord] + low[prefix_length:]
                break

        if chord[0].isupper():
            return transposed[0].upper() + transposed[1:]
        else:
            return transposed   

def transpose_sequence(chord_sequence, transposition):
    """ Transposes a sequence of chords a given number of halftones up.
    Chords with specified base sounds are split and the sound is transposed separately."""
    input_chords = [str(x) for x in chord_sequence.split()]
    output_chords = list()
    for chord in input_chords:
        if chord.find("/") != -1: # for chords with specified base sound
            transposed = "/".join([transpose_chord(x, transposition) for x in chord.split("/")])
        else:
            transposed = transpose_chord(chord, transposition)
        output_chords.append(transposed)
    return ' '.join(output_chords)

def transpose_lyrics(parsed_lyrics, transposition):
    """ Transposes a song represented as a list of paragraphs and returns result in the same format """
    result = []
    for paragraph in parsed_lyrics:
        section = []
        for (text, chords, is_indented, are_chords_extra) in paragraph:
            if chords.find("(") != -1:
                begin = chords.find("(")
                end = chords.find(")")
                if end == -1 or end < begin:
                    raise SyntaxError, "Incorrect '(' brackets in chords"
                core = chords[:begin].strip()
                bracketed = chords[begin+1:end].strip()
                transposed = "%s (%s)" % (transpose_sequence(core, transposition), transpose_sequence(bracketed, transposition)) 
            else:
                transposed = transpose_sequence(chords.strip(), transposition)
            section.append(
                (
                    text,
                    transposed,
                    is_indented,
                    are_chords_extra
                )
            )
        result.append(section)
    return result