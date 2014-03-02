from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView

import songs.views
import frontpage.views

admin.autodiscover()

urlpatterns = patterns(
    '',
    #obsolete paths redicrects
    url(r'^songs/song/(?P<song_id>\d+)/$', songs.views.obsolete_song),
    url(r'^songs/artist/(?P<artist_id>\d+)/$', songs.views.obsolete_artist),
    url(r'^songs/band/(?P<band_id>\d+)/$', songs.views.obsolete_band),
    #site sections
    url(r'^spiewnik/', include('songs.urls')),
    url(r'^blog/', include('blog.urls')),
    url(r'^artykuly/', include('articles.urls')),
    url(r'^wydarzenia/', include('events.urls')),
    url(r'^o-stronie/$', TemplateView.as_view(template_name="about.html")),
    url(r'^about/$', RedirectView.as_view(url="/o-stronie/")),
    url(r'^facebook/$', RedirectView.as_view(url="/o-stronie/")),
    #site-search index
    url(r'^index/', include('frontpage.index')),
    #admin
    url(r'^admin/', include(admin.site.urls)),
    #index
    url(r'^$', frontpage.views.SiteIndex.as_view(), name="index"),
)

from django.conf import settings

if settings.DEBUG:
    urlpatterns = patterns(
        '',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.ALL_STATIC_ROOT}),
        (r'^500/$', TemplateView.as_view(template_name='500.html')),
        (r'^404/$', TemplateView.as_view(template_name='404.html')),
    ) + urlpatterns
