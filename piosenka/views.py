from datetime import date, datetime

from django.contrib.auth.models import User
from django.views.generic import TemplateView

from articles.models import Article
from blog.models import Post
from content.models import filter_visible_to_user
from events.models import get_events_for
from songs.models import ArtistNote, Song, SongNote


class SiteIndex(TemplateView):
    template_name = "frontpage/index.html"
    POST_COUNT = 1
    SONG_COUNT = 8
    ANNOTATION_COUNT = 8

    def get_song_of_the_day(self):
        today = date.today()
        return (
            filter_visible_to_user(SongNote.objects.all(), self.request.user)
            .filter(date__isnull=False)
            .exclude(date_description="")
            .exclude(image="")
            .filter(date__day=today.day, date__month=today.month)
            .first()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["article"] = (
            Article.items_visible_to(self.request.user).order_by("-pub_date").first()
        )
        context["events"] = get_events_for(self.request.user)
        context["posts"] = Post.items_visible_to(self.request.user).order_by(
            "-pub_date"
        )[: SiteIndex.POST_COUNT]
        context["songs"] = Song.items_visible_to(self.request.user).order_by(
            "-pub_date"
        )[: SiteIndex.SONG_COUNT]
        context["song_of_the_day"] = self.get_song_of_the_day()
        context["annotation"] = (
            SongNote.items_visible_to(self.request.user).order_by("-pub_date").first()
        )
        song_notes = SongNote.items_visible_to(self.request.user).order_by("-pub_date")[
            : SiteIndex.ANNOTATION_COUNT
        ]
        artist_notes = ArtistNote.items_visible_to(self.request.user).order_by(
            "-pub_date"
        )[: SiteIndex.ANNOTATION_COUNT]
        notes = list(song_notes) + list(artist_notes)
        notes.sort(key=lambda x: x.pub_date, reverse=True)
        context["annotations"] = notes[: SiteIndex.ANNOTATION_COUNT]
        return context


class About(TemplateView):
    ARTICLE_FACTOR = 5
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authors = []
        for user in User.objects.filter(is_active=True):
            author = {}
            author["user"] = user
            author["annotations"] = (
                SongNote.items_live().filter(author=user).count()
                + ArtistNote.items_live().filter(author=user).count()
            )
            author["songs"] = Song.items_live().filter(author=user).count()
            author["articles"] = Article.items_live().filter(author=user).count()
            author["total"] = (
                author["annotations"]
                + author["songs"]
                + self.ARTICLE_FACTOR * author["articles"]
            )
            if author["total"]:
                authors.append(author)
        context["authors"] = sorted(authors, key=lambda k: k["total"], reverse=True)
        return context


class Format(TemplateView):
    template_name = "format.generated"


class Search(TemplateView):
    template_name = "search.html"
