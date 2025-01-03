from django.urls import include, path
from django.views.generic.base import RedirectView

from blog import views
from content import url_scheme

urlpatterns = [
    path("", views.PostIndex.as_view(), name="post_index"),
    path("post/<int:post_id>/", views.obsolete_post),
    path("dodaj/", views.AddPost.as_view(), name="add_post"),
    path(
        "<str:year>/<str:month>/<str:day>/<slug:slug>/",
        RedirectView.as_view(url="/blog/%(slug)s/", permanent=True),
    ),
    path(
        "<slug:slug>/",
        include(
            url_scheme.view_edit_review_approve(
                "post",
                views.ViewPost,
                views.EditPost,
                views.ReviewPost,
                views.ApprovePost,
            )
        ),
    ),
]
