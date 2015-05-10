from django.conf.urls import include, url

from blog import views


urlpatterns = [
    url(r'^$', views.PostIndex.as_view(), name='post_index'),
    url(r'^post/(?P<post_id>\d+)/$', views.obsolete_post),
    url(r'^dodaj/$', views.AddPost.as_view(), name='add_post'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/',
        include([
            url(r'^$', views.ViewPost.as_view(), name='post_detail'),
            url(r'^edytuj/$', views.EditPost.as_view(), name='edit_post'),
            url(r'^korekta/$', views.ReviewPost.as_view(),
                name='review_post'),
            url(r'^zatwierdz/$', views.ApprovePost.as_view(),
                name='approve_post'),
        ])),
]
