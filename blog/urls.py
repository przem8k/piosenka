from django.conf.urls import patterns, url
from blog.views import AddPost, EditPost, PostDetail, ApprovePost
from blog.views import PostIndex, obsolete_post


urlpatterns = patterns(
    'blog.views',
    url(r'^$', PostIndex.as_view(), name='post_index'),
    url(r'^post/(?P<post_id>\d+)/$', obsolete_post),
    url(r'^dodaj/$', AddPost.as_view(), name='add_post'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        PostDetail.as_view(), name='post_detail'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/'
        r'edytuj/$',
        EditPost.as_view(), name='edit_post'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/'
        r'zatwierdz/$',
        ApprovePost.as_view(), name='approve_post'),
)
