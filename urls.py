from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, re_path
from django.views.generic import TemplateView

import piosenka.views
import songs.views

admin.autodiscover()

urlpatterns = [
    # Songbook.
    re_path(r"^spiewnik/", include("songs.urls_entity")),
    re_path(r"^opracowanie/", include("songs.urls_song")),
    re_path(r"^adnotacja/", include("songs.urls_annotation")),
    re_path(r"^historia/", songs.views.CalendarView.as_view(), name="calendar"),
    # Other sections.
    re_path(r"^blog/", include("blog.urls")),
    re_path(r"^artykuly/", include("articles.urls")),
    re_path(r"^wydarzenia/", include("events.urls")),
    re_path(r"^o-stronie/$", piosenka.views.About.as_view(), name="about"),
    # Site-search index.
    re_path(r"^index/", include("piosenka.index")),
    # Search results.
    re_path(r"^szukaj/", piosenka.views.Search.as_view(), name="search"),
    # Admin and users.
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^redakcja/", include("piosenka.user_urls")),
    # Inspect.
    re_path(r"^inspect/", include("piosenka.inspect_urls")),
    # Frontpage.
    re_path(r"^$", piosenka.views.SiteIndex.as_view(), name="index"),
]

if settings.DEBUG:
    urlpatterns += (
        [
            re_path(r"^403/$", TemplateView.as_view(template_name="403.html")),
            re_path(r"^404/$", TemplateView.as_view(template_name="404.html")),
            re_path(r"^500/$", TemplateView.as_view(template_name="500.html")),
        ]
        + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
