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

from piosenka.forms import InvitationForm, JoinForm
from piosenka.mail import send_invitation_mail
from piosenka.models import Invitation


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


class InviteView(CreateView):
    model = Invitation
    form_class = InvitationForm
    template_name = "invite.html"

    @method_decorator(login_required)
    @method_decorator(permission_required("piosenka.invite", raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.extended_by = self.request.user
        ret = super().form_valid(form)

        send_invitation_mail(form.instance)
        messages.add_message(self.request, messages.INFO, "Zaproszenie wysłane.")
        logging.info(
            "%s invited %s to join" % (self.request.user, form.instance.email_address)
        )
        return ret

    def get_success_url(self):
        return reverse("index")


class JoinView(FormView):
    form_class = JoinForm
    template_name = "join.html"

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_anonymous:
            logging.warning("%s tried /join while signed in" % self.request.user)
            raise Http404
        return super().dispatch(*args, **kwargs)

    def get_invitation(self):
        invitation = Invitation.objects.get(
            invitation_key=self.kwargs["invitation_key"]
        )
        if not invitation.is_valid or invitation.expires_on < timezone.now():
            raise Http404
        return invitation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["invitation"] = self.get_invitation()
        return context

    def form_valid(self, form):
        invitation = self.get_invitation()
        invitation.is_valid = False
        invitation.save()

        user = User.objects.create_user(
            username=form.cleaned_data["username"],
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
            password=form.cleaned_data["password"],
            email=invitation.email_address,
        )
        user.save()

        everyone_group, _ = Group.objects.get_or_create(name="everyone")
        user.groups.add(everyone_group)

        logging.info("%s joined" % user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("hello")
