from django.conf.urls.defaults import *

from articles.views import *

urlpatterns = patterns('articles.views',
    url(r'^$', IndexView.as_view(), name="articles"),
    url(r'^(?P<slug>[-\w]+)/$', ArticleView.as_view(), name="article"),
)

