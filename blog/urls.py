from django.conf.urls import patterns, url
from blog.views import PostDetail, PostIndex, obsolete_post


urlpatterns = patterns(
    'blog.views',
    url(r'^$', PostIndex.as_view(), name="post_index"),
    url(r'^post/(?P<post_id>\d+)/$', obsolete_post),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        PostDetail.as_view(), name="post_detail"),
)
