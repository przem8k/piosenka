from django.conf.urls import url
from django.contrib.auth import views as auth_views

from piosenka import user_views

urlpatterns = [
    url(r'^do-korekty/', user_views.ToReview.as_view(), name='to_review'),
    url(
        r'^zaloguj/',
        auth_views.LoginView.as_view(template_name='hello.html'),
        name='hello'),
    url(r'^wyloguj/', auth_views.LogoutView.as_view(), name='goodbye'),
    url(
        r'^zmien-haslo/',
        user_views.ChangePassword.as_view(),
        name='change_password'),
    url(
        r'^nie-pamietam-hasla/',
        user_views.ResetPassword.as_view(),
        name='reset_password'),
    url(
        r'^nowe-haslo/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        user_views.ConfirmPasswordReset.as_view(),
        name='confirm_password_reset'),
    url(r'^zapros/', user_views.InviteView.as_view(), name='invite'),
    url(
        r'^dolacz/(?P<invitation_key>[-\w]+)/',
        user_views.JoinView.as_view(),
        name='join'),
]
