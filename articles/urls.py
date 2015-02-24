from django.conf.urls import patterns, url

from articles.views import AddArticle, ApproveArticle, ArticleView, EditArticle
from articles.views import IndexView

urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name='articles'),
    url(r'^dodaj/$', AddArticle.as_view(), name='add_article'),
    url(r'^(?P<slug>[-\w]+)/$', ArticleView.as_view(), name='article'),
    url(r'^(?P<slug>[-\w]+)/edytuj/$', EditArticle.as_view(),
        name='edit_article'),
    url(r'^(?P<slug>[-\w]+)/zatwierdz/$', ApproveArticle.as_view(),
        name='approve_article'),
)
