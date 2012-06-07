from django.template import RequestContext, Context, loader
from songs.models import Song, ArtistContribution, BandContribution
from artists.models import Artist, Band
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, Http404
from django.db.models import Q
from haystack.views import SearchView
from django.shortcuts import get_object_or_404, render

import string

def songs_context(request):
    url_segments = [x for x in request.path.split("/") if len(x) > 0]
    
    context = {}
    if len(url_segments) >= 3 and url_segments[0] == "spiewnik":
        context["artist_slug"] = url_segments[1]
        context["song_slug"] = url_segments[2]

    context["artists"] = Artist.objects.filter(display = True).order_by('lastname')
    context["bands"] = Band.objects.filter(display = True).order_by('name')
    return context

class LyricsParserMode:
    Regular = 0
    Recording = 1
    Replaying = 2

def parse_lyrics(lyrics):
    """
        returns parsed lyrics as a list of tuples (text, uniqueChords, repeatedChords)
    """
    result = []
    mode = LyricsParserMode.Regular
    recorded_section = None
    recorded_chords = []
    recordings = {}
    replayed_chords = []
    replay_index = -1
    for lineRaw in lyrics.split('\n'):
        line = lineRaw.strip()
        
        # break current recording
        if recorded_section != None and len(line) == 0:
            recordings[recorded_section] = recorded_chords
            recorded_section = None
            mode = LyricsParserMode.Regular
            
        # start new recording
        if len(line)>0 and line[0] == '#':
            recorded_section = line[1:]
            recorded_chords = []
            mode = LyricsParserMode.Recording
        elif len(line)>0 and line[0] == '@':
            replayed_chords = recordings[line[1:]]
            replay_index = 0
            mode = LyricsParserMode.Replaying
        else:
            textPart = ""
            chordsPart = ""
            extraPart = ""
            chordsStart = line.find("[")
            extraStart = line.find("{")
            if chordsStart != -1:
                textPart = line[0:chordsStart]
                chordsPart = line[chordsStart+1:len(line)-1]
            elif extraStart != -1:
                textPart = line[0:extraStart]
                extraPart = line[extraStart+1:len(line)-1]
            else:
                textPart = line
                
            if mode == LyricsParserMode.Recording:
                recorded_chords.append(chordsPart)
            elif mode == LyricsParserMode.Replaying:
                if replay_index < len(replayed_chords) and len(chordsPart) == 0:
                    extraPart = replayed_chords[replay_index]
                replay_index = replay_index + 1 
            result.append((textPart,chordsPart,extraPart))
    if recorded_section != None:
        recordings[recorded_section] = recorded_chords
        recorded_section = None
    return result

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

def transpose(chord_sequence, transposition):
    """ Transposes a sequence of chords a given number of halftones up """
    input_chords = [str(x) for x in chord_sequence.split()]
    output_chords = list()
    for chord in input_chords:
        low = chord[0].lower() + chord[1:]

        transposed = "??"
        for prefix_length in [3,2,1]:
            if len(low) >= prefix_length and low[:prefix_length] in KEYS_TO_ORD:
                new_ord = (KEYS_TO_ORD[low[:prefix_length]] + transposition) % 12
                transposed = ORD_TO_KEY[new_ord] + low[prefix_length:]
                break

        if chord[0].isupper():
            output_chords.append(transposed[0].upper() + transposed[1:])
        else:
            output_chords.append(transposed)
    return ' '.join(output_chords)

def render_html(lyrics_data, any_chords, extra_chords, extra_chords_trigger, transposition = 0):
    formatedLines = ["<table>",]
    for entry in lyrics_data:
        textPart = entry[0]
        basicPart = entry[1]
        extraPart = entry[2]
        
        if any_chords:
            if extra_chords and len(extraPart) > 0:
                if extra_chords_trigger:
                    renderedChords = "<span class=\"extra-chords\">%s</span>" % (
                        transpose(extraPart, transposition),
                    )
                else:
                    renderedChords = transpose(extraPart, transposition)
            elif len(basicPart) > 0:
                renderedChords = transpose(basicPart, transposition)
            else:
                renderedChords = ""
        else:
            renderedChords = ""

        if len(textPart) + len(basicPart) + len(extraPart) > 0:
            if len(textPart) > 0 and textPart[0] == ">":
                formatedLines.append(u"<tr><td class=\"indented\">{0}</td><td class=\"indented\"><b>{1}</b></td></tr>".format(textPart[1:], renderedChords))
            else:
                formatedLines.append(u"<tr><td>{0}</td><td class=\"indented\"><b>{1}</b></td></tr>".format(textPart, renderedChords))
        else:
            formatedLines.append("</table>\n<br />\n<table>")
    formatedLines.append("</table>")
    return string.join(formatedLines, "\n")
def index(request):
    template = loader.get_template('songs.html')
    cc = common_context()
    return HttpResponse(template.render(RequestContext(request, cc)))

class SongMode:
    DISPLAY = 0
    PRINT_TEXT_ONLY = 1
    PRINT_BASIC_CHORDS = 2
    PRINT_ALL_CHORDS = 3

def song_engine(request, song, mode):
    if mode == SongMode.DISPLAY:
        template = loader.get_template('songs_song.html')
    else:
        template = loader.get_template('songs_song_print.html')
    
    if not song.lyrics_html_for_display:
        song.render()
    cc = {}
    cc['song'] = song
    cc['section'] = 'songs'
    if mode == SongMode.DISPLAY:
        cc['lyrics'] = song.lyrics_html_for_display
        if song.lyrics_contain_extra_chords:
            cc['extra'] = True
    elif mode == SongMode.PRINT_TEXT_ONLY:
        cc['lyrics'] = song.lyrics_html_text_only
    elif mode == SongMode.PRINT_BASIC_CHORDS:
        cc['lyrics'] = song.lyrics_html_basic_chords
    elif mode == SongMode.PRINT_ALL_CHORDS:
        cc['lyrics'] = song.lyrics_html_all_chords
    cc['textContributions'] = ArtistContribution.objects.filter(song = song, texted = True);
    cc['translationContributions'] = ArtistContribution.objects.filter(song = song, translated = True);
    cc['musicContributions'] = ArtistContribution.objects.filter(song = song, composed = True)
    cc['performanceContributions'] = ArtistContribution.objects.filter(song = song, performed = True)
    cc['bandContributions'] = BandContribution.objects.filter(song = song, performed = True)
    cc['external_links'] = [(x.artist,x.artist.website) for x in ArtistContribution.objects.filter(song=song) if x.artist.website != None and len(x.artist.website) > 0 ] + [(x.band,x.band.website) for x in BandContribution.objects.filter(song=song) if x.band.website != None and len(x.band.website) > 0] 
    cc['request'] = request
    return HttpResponse(template.render(RequestContext(request,cc)))
    
def song(request, slug, mode):
    piece = get_object_or_404(Song, slug = slug)
    return song_engine(request,piece,mode)
    
def artist_song(request, artist_slug, song_slug, mode):
    piece = get_object_or_404(Song, slug = song_slug)
    artist = None
    for entry in ArtistContribution.objects.filter(song = piece):
        if entry.artist.slug == artist_slug:
            artist = entry.artist
    for entry in BandContribution.objects.filter(song = piece):
        if entry.band.slug == artist_slug:
            artist = entry.band
    
    if not artist:
        raise Http404()
    return song_engine(request,piece,mode) 

def redirect_to_song(request, song_slug):
    piece = get_object_or_404(Song, slug = song_slug)
    artists = ArtistContribution.objects.filter(song = piece)
    bands = BandContribution.objects.filter(song = piece)
    if len(artists) > 0:
        artist = artists[0].artist
    elif len(bands) > 0:
        artist = bands[0].band
    else:
        raise Http404()        
    return HttpResponsePermanentRedirect("/spiewnik/%s/%s/" % (artist.slug, piece.slug,))

def obsolete_song(request, song_id):
    song = get_object_or_404(Song, pk = song_id)
    return redirect_to_song(request, song.slug)

def artist(request, slug, template_name="songs/list.html"):
    if Artist.objects.filter(slug = slug).count() > 0:
        guy = Artist.objects.get(slug = slug)
        songs = ArtistContribution.objects.filter(artist = guy).order_by('song__title')
    else:
        guy = get_object_or_404(Band, slug = slug)
        songs = BandContribution.objects.filter(band = guy).order_by('song__title')

    if not request.user.is_staff:
        songs = songs.filter(song__published = True)

    return render(request, template_name, {'section' : 'songs', 'songs': songs, 'title': guy.__unicode__(), 'artist': guy})

def obsolete_artist(request, artist_id):
    artist = get_object_or_404(Artist, pk = artist_id)
    return HttpResponsePermanentRedirect("/spiewnik/%s/" % (artist.slug,) )
    
def obsolete_band(request, band_id):
    band = get_object_or_404(Band, pk = band_id)
    return HttpResponsePermanentRedirect("/spiewnik/%s/" % (band.slug,) )

class SongSearchView(SearchView):
    def __name__(self):
        return "SongSearchView"

    #def extra_context(self):
    #    extra = super(SongSearchView, self).extra_context()
    #    return common_context()
