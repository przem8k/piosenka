from django.conf.urls import patterns, url

from articles.views import ArticleView, IndexView

urlpatterns = patterns(
    'articles.views',
    url(r'^$', IndexView.as_view(), name="articles"),
    url(r'^(?P<slug>[-\w]+)/$', ArticleView.as_view(), name="article"),
)
