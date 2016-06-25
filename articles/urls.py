from django.conf.urls import include, url

from articles import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(),
        name='articles'),
    url(r'^dodaj/$', views.AddArticle.as_view(),
        name='add_article'),
    url(r'^(?P<slug>[-\w]+)/',
        include([
            url(r'^$', views.ViewArticle.as_view(),
                name='view_article'),
            url(r'^edytuj/$',
                views.EditArticle.as_view(),
                name='edit_article'),
            url(r'^korekta/$',
                views.ReviewArticle.as_view(),
                name='review_article'),
            url(r'^zatwierdz/$',
                views.ApproveArticle.as_view(),
                name='approve_article'),
        ])),
]
