import string

from django.template import RequestContext, Context, loader
from songs.models import Song, ArtistContribution, BandContribution
from artists.models import Artist, Band
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, Http404
from django.db.models import Q
from haystack.views import SearchView
from django.shortcuts import get_object_or_404, render

from songs.transpose import transpose_lyrics
from songs.parse import parse_lyrics

def songs_context(request):
    url_segments = [x for x in request.path.split("/") if len(x) > 0]
    
    context = {}
    if len(url_segments) >= 3 and url_segments[0] == "spiewnik":
        context["artist_slug"] = url_segments[1]
        context["song_slug"] = url_segments[2]

    context["artists"] = Artist.objects.filter(display = True).order_by('lastname')
    context["bands"] = Band.objects.filter(display = True).order_by('name')
    return context

class SongMode:
    DISPLAY = 0
    PRINT_TEXT_ONLY = 1
    PRINT_BASIC_CHORDS = 2
    PRINT_ALL_CHORDS = 3

def render_lyrics(lyrics, mode, template_name="songs/lyrics.html"):
    context = {
        "lyrics": lyrics,
        "any_chords": mode != SongMode.PRINT_TEXT_ONLY,
        "distinguish_extra_chords": mode != SongMode.PRINT_ALL_CHORDS,
    }
    template = loader.get_template(template_name)
    return template.render(Context(context))

def index(request):
    template = loader.get_template('songs.html')
    cc = common_context()
    return HttpResponse(template.render(RequestContext(request, cc)))

def song(request, song, mode, transposition = 0):
    if mode == SongMode.DISPLAY:
        template_name = 'songs_song.html'
    else:
        template_name = 'songs_song_print.html'

    external_links = [(x.artist,x.artist.website) for x in 
        ArtistContribution.objects.filter(song=song) if 
        x.artist.website != None and len(x.artist.website) > 0 
    ] + [(x.band,x.band.website) for x in 
        BandContribution.objects.filter(song=song) if 
        x.band.website != None and len(x.band.website) > 0
    ]

    context = {
        'song' : song,
        'section' : 'songs',
        'extra_trigger' : mode == SongMode.DISPLAY,
        'lyrics' : render_lyrics(
            transpose_lyrics(
                parse_lyrics(song.lyrics),
                transposition
            ),
            mode
        ),
        'textContributions' : ArtistContribution.objects.filter(song = song, texted = True),
        'translationContributions' : ArtistContribution.objects.filter(song = song, translated = True),
        'musicContributions' : ArtistContribution.objects.filter(song = song, composed = True),
        'performanceContributions' : ArtistContribution.objects.filter(song = song, performed = True),
        'bandContributions' : BandContribution.objects.filter(song = song, performed = True),
        'external_links' : external_links,
    }
    return render(request, template_name, context)

def song_by_unknown(request, slug, mode):
    piece = get_object_or_404(Song, slug = slug)
    return song(request,piece,mode)
    
def song_of_artist(request, artist_slug, song_slug, mode):
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
    return song(request,piece,mode) 

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
