from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.views.generic import TemplateView

from articles.models import Article
from blog.models import Post
from events.models import Event
from frontpage.models import CarouselItem
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
        context['carousel_items'] = CarouselItem.objects.filter(archived=False)
        context['events'] = Event.current.all()
        context['post'] = Post.objects.all().order_by('-date')[0]
        context['songs'] = songs
        return context


class About(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super(About, self).get_context_data(**kwargs)
        authors = []
        for user in User.objects.filter(is_active=True):
            author = {}
            author['user'] = user
            author['songs'] = Song.po.filter(author=user).count()
            author['articles'] = Article.po.filter(author=user).count()
            author['events'] = Event.po.filter(author=user).count()
            author['total'] = author['songs'] + author['articles'] + author['events']
            if author['total']:
                authors.append(author)
        context['authors'] = sorted(authors, key=lambda k: k['total'], reverse=True)
        return context
