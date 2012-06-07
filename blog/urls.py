from django.conf.urls.defaults import *
from blog.views import *

urlpatterns = patterns('blog.views',
    url(r'^$', IndexView.as_view(), name="blog"),
    url(r'^post/(?P<post_id>\d+)/$', obsolete_post),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', PostView.as_view(), name="post"),
)
