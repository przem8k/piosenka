from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView

import piosenka.views
import songs.obsolete

admin.autodiscover()

urlpatterns = [
    # Obsolete paths redicrects.
    url(r'^songs/song/(?P<song_id>\d+)/$', songs.obsolete.obsolete_song),
    url(r'^about/$', RedirectView.as_view(url="/o-stronie/", permanent=True)),
    url(r'^facebook/$', RedirectView.as_view(url="/o-stronie/",
                                             permanent=True)),
    # Songbook.
    url(r'^spiewnik/', include('songs.urls_entity')),
    url(r'^opracowanie/', include('songs.urls_song')),
    url(r'^adnotacja/', include('songs.urls_annotation')),
    # Other sections.
    url(r'^blog/', include('blog.urls')),
    url(r'^artykuly/', include('articles.urls')),
    url(r'^wydarzenia/', include('events.urls')),
    url(r'^o-stronie/$', piosenka.views.About.as_view(), name="about"),
    url(r'^o-stronie/format-opracowan/$', piosenka.views.Format.as_view(),
        name="format"),
    # Site-search index.
    url(r'^index/', include('piosenka.index')),
    # Admin and users.
    url(r'^admin/', include(admin.site.urls)),
    url(r'^do-korekty/', piosenka.views.ToReview.as_view(), name="to_review"),
    url(r'^zaloguj/', piosenka.views.Hello.as_view(), name="hello"),
    url(r'^wyloguj/', piosenka.views.Goodbye.as_view(), name="goodbye"),
    url(r'^zmien-haslo/', piosenka.views.ChangePassword.as_view(),
        name="change_password"),
    url(r'^zapros/', piosenka.views.InviteView.as_view(),
        name='invite'),
    # Frontpage.
    url(r'^$', piosenka.views.SiteIndex.as_view(), name="index"),
]

from django.conf import settings

if settings.DEBUG:
    urlpatterns = [
        url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.SERVE_DIRECTLY_ROOT}),
        url(r'^500/$', TemplateView.as_view(template_name='500.html')),
        url(r'^404/$', TemplateView.as_view(template_name='404.html')),
    ] + urlpatterns
