from django.conf.urls import include, url

from blog import views
from content import url_scheme

urlpatterns = [
    url(r'^$', views.PostIndex.as_view(),
        name='post_index'),
    url(r'^post/(?P<post_id>\d+)/$', views.obsolete_post),
    url(r'^dodaj/$', views.AddPost.as_view(),
        name='add_post'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/',
        include(url_scheme.view_edit_review_approve(
            'post', views.ViewPost, views.EditPost, views.ReviewPost,
            views.ApprovePost)))
]
