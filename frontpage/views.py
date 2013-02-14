from django.views.generic import TemplateView
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType


from blog.models import Post
from events.models import Event
from songs.models import Song

def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None

class SiteIndex(TemplateView):
    template_name = "frontpage/index.html"
    song_count = 10

    def get_context_data(self, **kwargs):
        song_type = ContentType.objects.get(app_label="songs", model="song")
        entries = LogEntry.objects.filter(content_type=song_type, action_flag=ADDITION).order_by("-action_time")[:SiteIndex.song_count]
        songs = [(x.action_time, get_or_none(Song, pk=x.object_id)) for x in entries if get_or_none(Song, pk=x.object_id) != None]

        context = super(SiteIndex, self).get_context_data(**kwargs)
        context['post'] = Post.objects.all().order_by('-date')[0]
        context['events'] = Event.current.all()
        context['songs'] = songs
        return context
