from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView

import songs.views
import frontpage.views

admin.autodiscover()

urlpatterns = patterns('',
    #obsolete paths redicrects
    url(r'^songs/song/(?P<song_id>\d+)/$', songs.views.obsolete_song),
    url(r'^songs/artist/(?P<artist_id>\d+)/$', songs.views.obsolete_artist),
    url(r'^songs/band/(?P<band_id>\d+)/$', songs.views.obsolete_band),
    #site sections
    url(r'^spiewnik/', include('songs.urls')),
    url(r'^blog/', include('blog.urls')),
    url(r'^wydarzenia/', include('events.urls')),
    url(r'^o-stronie/$', TemplateView.as_view(template_name="about.html")),
    url(r'^about/$', RedirectView.as_view(url="/o-stronie/")),
    url(r'^facebook/$', RedirectView.as_view(url="/o-stronie/")),
    #admin
    url(r'^admin/', include(admin.site.urls)),
    #index
    url(r'^$', frontpage.views.IndexView.as_view()),
)

from django.conf import settings

if settings.DEBUG:
    urlpatterns = patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    ) + patterns('',
        (r'^500/$', 'django.views.generic.simple.direct_to_template', {'template': '500.html'}),
        (r'^404/$', 'django.views.generic.simple.direct_to_template', {'template': '404.html'}),
    ) + urlpatterns
