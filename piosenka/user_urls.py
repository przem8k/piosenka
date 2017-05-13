from django.conf.urls import url

from piosenka import user_views

urlpatterns = [
    url(r'^do-korekty/', user_views.ToReview.as_view(), name='to_review'),
    url(r'^zaloguj/', user_views.Hello.as_view(), name='hello'),
    url(r'^wyloguj/', user_views.Goodbye.as_view(), name='goodbye'),
    url(
        r'^zmien-haslo/',
        user_views.ChangePassword.as_view(),
        name='change_password'),
    url(r'^zapros/', user_views.InviteView.as_view(), name='invite'),
    url(
        r'^dolacz/(?P<invitation_key>[-\w]+)/',
        user_views.JoinView.as_view(),
        name='join'),
]
