from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView

import frontpage.views
import songs.obsolete

admin.autodiscover()

urlpatterns = patterns(
    '',
    # Obsolete paths redicrects.
    url(r'^songs/song/(?P<song_id>\d+)/$', songs.obsolete.obsolete_song),
    url(r'^about/$', RedirectView.as_view(url="/o-stronie/")),
    url(r'^facebook/$', RedirectView.as_view(url="/o-stronie/")),
    # Songbook.
    url(r'^spiewnik/', include('songs.entity_urls')),
    url(r'^opracowanie/', include('songs.song_urls')),
    # Other sections.
    url(r'^blog/', include('blog.urls')),
    url(r'^artykuly/', include('articles.urls')),
    url(r'^wydarzenia/', include('events.urls')),
    url(r'^o-stronie/$', frontpage.views.About.as_view(), name="about"),
    # Site-search index.
    url(r'^index/', include('frontpage.index')),
    # Admin and users.
    url(r'^admin/', include(admin.site.urls)),
    url(r'^zaloguj/', frontpage.views.Hello.as_view(), name="hello"),
    url(r'^wyloguj/', frontpage.views.Goodbye.as_view(), name="goodbye"),
    # Frontpage.
    url(r'^$', frontpage.views.SiteIndex.as_view(), name="index"),
)

from django.conf import settings

if settings.DEBUG:
    urlpatterns = patterns(
        '',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.SERVE_DIRECTLY_ROOT}),
        (r'^500/$', TemplateView.as_view(template_name='500.html')),
        (r'^404/$', TemplateView.as_view(template_name='404.html')),
    ) + urlpatterns
