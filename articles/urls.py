from django.urls import include, re_path

from articles import views
from content import url_scheme

urlpatterns = [
    re_path(r"^$", views.IndexView.as_view(), name="articles"),
    re_path(r"^dodaj/$", views.AddArticle.as_view(), name="add_article"),
    re_path(
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
