import logging
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.views import (PasswordResetConfirmView,
                                       PasswordResetView)
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, View
from django.views.generic.edit import CreateView, FormView

class ResetPassword(PasswordResetView):
    template_name = "reset_password.html"
    success_url = reverse_lazy("index")
    subject_template_name = "mail/password_reset.subject.txt"
    email_template_name = "mail/password_reset.txt"
    html_email_template_name = "mail/password_reset.html"

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, "Dziękujemy. Sprawdź podany adres email."
        )
        return super().form_valid(form)


class ConfirmPasswordReset(PasswordResetConfirmView):
    template_name = "confirm_password_reset.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, "Dziękujemy. Hasło zostało zmienione."
        )
        return super().form_valid(form)


class ChangePassword(FormView):
    form_class = PasswordChangeForm
    template_name = "change_password.html"
    success_url = reverse_lazy("index")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ToReview(TemplateView):
    template_name = "to_review.html"

    @method_decorator(login_required)
    @method_decorator(permission_required("content.review", raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)