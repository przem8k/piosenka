from django.contrib.auth import views as auth_views
from django.urls import re_path

from piosenka import user_views

urlpatterns = [
    re_path(r"^do-korekty/", user_views.ToReview.as_view(), name="to_review"),
    re_path(
        r"^zaloguj/",
        auth_views.LoginView.as_view(template_name="hello.html"),
        name="hello",
    ),
    re_path(r"^wyloguj/", auth_views.LogoutView.as_view(), name="goodbye"),
    re_path(
        r"^zmien-haslo/", user_views.ChangePassword.as_view(), name="change_password"
    ),
    re_path(
        r"^nie-pamietam-hasla/",
        user_views.ResetPassword.as_view(),
        name="reset_password",
    ),
    re_path(
        r"^nowe-haslo/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/",
        user_views.ConfirmPasswordReset.as_view(),
        name="confirm_password_reset",
    ),
    re_path(r"^zapros/", user_views.InviteView.as_view(), name="invite"),
    re_path(
        r"^dolacz/(?P<invitation_key>[-\w]+)/",
        user_views.JoinView.as_view(),
        name="join",
    ),
]
