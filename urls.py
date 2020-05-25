import django.views.static
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf.urls.static import static

import piosenka.views
import songs.views

admin.autodiscover()

urlpatterns = [
    # Songbook.
    url(r'^spiewnik/', include('songs.urls_entity')),
    url(r'^opracowanie/', include('songs.urls_song')),
    url(r'^adnotacja/', include('songs.urls_annotation')),
    url(r'^historia/', songs.views.CalendarView.as_view(), name='calendar'),
    # Other sections.
    url(r'^blog/', include('blog.urls')),
    url(r'^artykuly/', include('articles.urls')),
    url(r'^wydarzenia/', include('events.urls')),
    url(r'^o-stronie/$', piosenka.views.About.as_view(), name='about'),
    url(
        r'^o-stronie/format-opracowan/$',
        piosenka.views.Format.as_view(),
        name='format'),
    # Site-search index.
    url(r'^index/', include('piosenka.index')),
    # Search results.
    url(r'^szukaj/', piosenka.views.Search.as_view(), name='search'),
    # Admin and users.
    url(r'^admin/', admin.site.urls),
    url(r'^redakcja/', include('piosenka.user_urls')),
    # Inspect.
    url(r'^inspect/', include('piosenka.inspect_urls')),
    # Frontpage.
    url(r'^$', piosenka.views.SiteIndex.as_view(), name='index'),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^403/$', TemplateView.as_view(template_name='403.html')),
        url(r'^404/$', TemplateView.as_view(template_name='404.html')),
        url(r'^500/$', TemplateView.as_view(template_name='500.html')),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
