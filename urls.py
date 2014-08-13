from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView

import frontpage.views
import songs.obsolete
import songs.views

admin.autodiscover()

urlpatterns = patterns(
    '',
    #obsolete paths redicrects
    url(r'^songs/song/(?P<song_id>\d+)/$', songs.obsolete.obsolete_song),
    url(r'^songs/artist/(?P<artist_id>\d+)/$', songs.obsolete.obsolete_artist),
    url(r'^songs/band/(?P<band_id>\d+)/$', songs.obsolete.obsolete_band),
    url(r'^about/$', RedirectView.as_view(url="/o-stronie/")),
    url(r'^facebook/$', RedirectView.as_view(url="/o-stronie/")),
    #site sections
    url(r'^spiewnik/', include('songs.urls')),
    url(r'^blog/', include('blog.urls')),
    url(r'^artykuly/', include('articles.urls')),
    url(r'^wydarzenia/', include('events.urls')),
    url(r'^o-stronie/$', frontpage.views.About.as_view(), name="about"),
    #site-search index
    url(r'^index/', include('frontpage.index')),
    #admin and users
    url(r'^admin/', include(admin.site.urls)),
    url(r'^zaloguj/', frontpage.views.Hello.as_view(), name="hello"),
    url(r'^wyloguj/', frontpage.views.Goodbye.as_view(), name="goodbye"),
    # frontpage
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
