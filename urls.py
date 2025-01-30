from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, re_path
from django.views.generic import TemplateView

import piosenka.views

admin.autodiscover()

urlpatterns = [
    # Site-search index.
    re_path(r"^index/", include("piosenka.index")),
    # Search results.
    re_path(r"^szukaj/", piosenka.views.Search.as_view(), name="search"),
    # Admin and users.
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^redakcja/", include("piosenka.user_urls")),
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
