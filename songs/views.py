import json

from django.core.urlresolvers import reverse_lazy
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, RedirectView
from django.views.generic.edit import CreateView, UpdateView

from artists.models import Entity
from frontpage.views import CheckAuthorshipMixin, CheckLoginMixin, ManageInlineFormsetMixin
from songs.forms import SongForm, ContributionFormSet
from songs.lyrics import render_lyrics
from songs.models import Song, EntityContribution


INITIAL_LYRICS = \
"""#zw
Pierwszy wers zwrotki [C G F E]
Drugi wers zwrotki [a C]
Trzeci wers zwrotki [a C]
Czwarty wers zwrotki [F E]

#ref
>Obława, obława, na młode wilki obława [a C G C]
>Te dzikie, zapalczywe, w gęstym lesie wychowane [F E]
>Krąg w śniegu wydeptany, w tym kręgu plama krwawa [a C G C]
>Ciała wilcze kłami gończych psów szarpane! [F E]

@zw
Druga zwrotka o tych samych akordach
Co pierwsza zwrotka
Kolejny wers, kolejny wers
I jeszcze jeden i jeszcze raz
"""


def get_song_by_entity_or_404(song_slug, entity_slug):
    song = get_object_or_404(Song, slug=song_slug)
    entity = get_object_or_404(Entity, slug=entity_slug)
    # verify that the song was reached via proper artist or band
    if EntityContribution.objects.filter(song=song, entity=entity).count() == 0:
        raise Http404()
    return song


class SongRedirectView(RedirectView):
    """ Displays a songs by default, returns transposed lyrics part in json if asked. """

    def get_redirect_url(self, *args, **kwargs):
        song = get_song_by_entity_or_404(kwargs['song_slug'], kwargs['entity_slug'])
        return song.get_absolute_url()


class BaseMenuView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(BaseMenuView, self).get_context_data(**kwargs)
        context["bards"] = Entity.objects.filter(featured=True, kind=Entity.TYPE_TEXTER)
        context["composers"] = Entity.objects.filter(featured=True, kind=Entity.TYPE_COMPOSER)
        context["translators"] = Entity.objects.filter(featured=True, kind=Entity.TYPE_TRANSLATOR)
        context["performers"] = Entity.objects.filter(featured=True, kind=Entity.TYPE_PERFORMER)
        context["foreigners"] = Entity.objects.filter(featured=True, kind=Entity.TYPE_FOREIGN)
        context["bands"] = Entity.objects.filter(featured=True, kind=Entity.TYPE_BAND)
        return context


class IndexView(BaseMenuView):
    template_name = "songs/index.html"


class EntityView(BaseMenuView):
    """ Lists the songs associated with the given Entity object. """
    template_name = "songs/list.html"

    def get_context_data(self, **kwargs):
        slug = kwargs['slug']
        entity = get_object_or_404(Entity, slug=slug)
        songs = [x.song for x in (EntityContribution.objects.filter(entity=entity,
                                                                    song__published=True)
                                  .select_related('song')
                                  .order_by('song__title'))]
        if not songs:
            raise Http404()
        context = super(EntityView, self).get_context_data(**kwargs)
        context['songs'] = songs
        context['entity'] = entity
        return context


class SongView(TemplateView):
    """ Displays a songs by default, returns transposed lyrics part in json if asked. """
    template_name = 'songs/song.html'

    def get_context_data(self, **kwargs):
        context = super(SongView, self).get_context_data(**kwargs)
        song = get_object_or_404(Song, new_slug=kwargs['song_slug'])
        if 'transposition' in kwargs:
            context['json'] = True
            transposition = int(kwargs['transposition'])
            context['transposition'] = transposition
        else:
            transposition = 0
        context['song'] = song
        context['lyrics'] = render_lyrics(song.lyrics, transposition)
        context['can_edit'] = self.request.user.is_active and (
            self.request.user.is_staff or self.request.user == self.object.author)
        return context

    def render_to_response(self, context):
        if context.get('json'):
            return self.get_lyrics_as_json(context)
        return super(SongView, self).render_to_response(context)

    def get_lyrics_as_json(self, context):
        payload = {'lyrics': context['lyrics'],
                   'transposition': context['transposition']}
        return HttpResponse(json.dumps(payload),
                            content_type='application/json')


class AddSong(CheckLoginMixin, ManageInlineFormsetMixin, CreateView):
    model = Song
    form_class = SongForm
    template_name = "songs/add_edit_song.html"

    def get_initial(self):
        return {
            'lyrics': INITIAL_LYRICS,
        }

    def get_managed_formset_class(self):
        return ContributionFormSet

    def form_valid(self, form):
        contributions = super(AddSong, self).get_managed_formset()
        if not contributions.is_valid():
            return self.form_invalid(form)
        form.instance.author = self.request.user
        contributions.instance = form.save()
        contributions.save()
        return super(AddSong, self).form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class EditSong(CheckAuthorshipMixin, ManageInlineFormsetMixin, UpdateView):
    model = Song
    form_class = SongForm
    template_name = "songs/add_edit_song.html"

    def get_object(self):
        return get_object_or_404(Song, new_slug=self.kwargs['song_slug'])

    def get_managed_formset_class(self):
        return ContributionFormSet

    def form_valid(self, form):
        contributions = super(EditSong, self).get_managed_formset()
        if not contributions.is_valid():
            return self.form_invalid(form)
        contributions.instance = form.save()
        contributions.save()
        return super(EditSong, self).form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()
