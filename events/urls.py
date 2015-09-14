from django.conf.urls import include, url

from events import views

urlpatterns = [
    url(r'^$', views.EventIndex.as_view(), name="event_index"),
    url(r'^(?P<year>\d{4})/', include([
        url(r'^$', views.YearArchive.as_view(), name="event_year"),
        url(r'^(?P<month>\d{2})/', include([
            url(r'^$', views.MonthArchiveRedirect.as_view(),
                name="event_month_redirect"),
            url(r'^(?P<day>\d{2})/(?P<slug>[-\w]+)/', include([
                url(r'^$', views.ViewEvent.as_view(), name="view_event"),
                url(r'^edytuj/$', views.EditEvent.as_view(), name="edit_event"),
                url(r'^korekta/$', views.ReviewEvent.as_view(),
                    name="review_event"),
                url(r'^zatwierdz/$', views.ApproveEvent.as_view(),
                    name="approve_event")
                ])),
            ])),
        ])),
    url(r'^dodaj/$', views.AddEvent.as_view(), name="add_event"),
    url(r'^wykonawca/(?P<slug>[-\w]+)/$', views.ViewPerformer.as_view(),
        name="view_performer"),
    url(r'^(?P<slug>[-\w]+)/$', views.VenueDetail.as_view(),
        name="venue_detail"),
]
