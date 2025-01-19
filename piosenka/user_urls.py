from django.contrib.auth import views as auth_views
from django.urls import path

from piosenka import user_views

urlpatterns = [
    path(r"do-korekty/", user_views.ToReview.as_view(), name="to_review"),
    path(
        r"zaloguj/",
        auth_views.LoginView.as_view(template_name="hello.html"),
        name="hello",
    ),
    path(r"wyloguj/", auth_views.LogoutView.as_view(), name="goodbye"),
    path(r"zmien-haslo/", user_views.ChangePassword.as_view(), name="change_password"),
    path(
        r"nie-pamietam-hasla/",
        user_views.ResetPassword.as_view(),
        name="reset_password",
    ),
    path(
        r"nowe-haslo/<str:uidb64>/<str:token>/",
        user_views.ConfirmPasswordReset.as_view(),
        name="confirm_password_reset",
    ),
]
