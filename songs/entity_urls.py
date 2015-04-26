from django.conf.urls import include, url
from django.views.generic import RedirectView

from songs import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="songbook"),
    url(r'^(?P<slug>[-\w]+)/$', views.EntityView.as_view(),
        name="songbook_entity"),
    # Obsolete url redirects.
    url(r'^(?P<entity_slug>[-\w]+)/(?P<slug>[-\w]+)/', include([
        url(r'^$', views.SongRedirectView.as_view()),
        url(r'^drukuj/$', RedirectView.as_view(
            url='/spiewnik/%(entity_slug)s/%(slug)s/')),
        ])),
]
