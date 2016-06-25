from django.conf.urls import include, url

from songs import views

urlpatterns = [
    url(r'^(?P<slug>[-\w]+)/',
        include([
            url(r'^edytuj/$',
                views.EditAnnotation.as_view(),
                name="edit_annotation"),
            url(r'^korekta/$',
                views.ReviewAnnotation.as_view(),
                name="review_annotation"),
            url(r'^zatwierdz/$',
                views.ApproveAnnotation.as_view(),
                name="approve_annotation"),
        ])),
]
