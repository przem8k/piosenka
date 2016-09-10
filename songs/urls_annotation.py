from django.conf.urls import include, url

from content import url_scheme
from songs import views

urlpatterns = [
    url(r'^(?P<slug>[-\w]+)/',
        include(url_scheme.edit_review_approve(
                            'annotation', views.EditAnnotation,
                            views.ReviewAnnotation, views.ApproveAnnotation))),
]
