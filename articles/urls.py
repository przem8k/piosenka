from django.conf.urls import include, url

from articles import views
from content import url_scheme

urlpatterns = [
    url(r"^$", views.IndexView.as_view(), name="articles"),
    url(r"^dodaj/$", views.AddArticle.as_view(), name="add_article"),
    url(
        r"^(?P<slug>[-\w]+)/",
        include(
            url_scheme.view_edit_review_approve(
                "article",
                views.ViewArticle,
                views.EditArticle,
                views.ReviewArticle,
                views.ApproveArticle,
            )
        ),
    ),
]
