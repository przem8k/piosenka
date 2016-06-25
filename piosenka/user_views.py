from datetime import datetime
import logging

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import login, logout
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, Http404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView
from django.views.generic.edit import FormView, CreateView

from piosenka.forms import InvitationForm, JoinForm
from piosenka.models import Invitation
from piosenka.mail import send_invitation_mail

_action_logger = logging.getLogger('actions')


class Hello(FormView):
    form_class = AuthenticationForm
    template_name = "hello.html"
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET and 'next' in self.request.GET:
            context['next'] = self.request.GET['next']
        return context

    def form_valid(self, form):
        login(self.request, form.get_user())
        if self.request.GET and 'next' in self.request.GET:
            return HttpResponseRedirect(self.request.GET['next'])
        return super().form_valid(form)


class Goodbye(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('index'))


class ChangePassword(FormView):
    form_class = PasswordChangeForm
    template_name = "change_password.html"
    success_url = reverse_lazy('index')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ToReview(TemplateView):
    template_name = "to_review.html"

    @method_decorator(login_required)
    @method_decorator(permission_required('content.review',
                                          raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class InviteView(CreateView):
    model = Invitation
    form_class = InvitationForm
    template_name = "invite.html"

    @method_decorator(login_required)
    @method_decorator(permission_required('piosenka.invite',
                                          raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.extended_by = self.request.user
        ret = super().form_valid(form)

        send_invitation_mail(form.instance)
        _action_logger.info('%s invited %s to join' %
                            (self.request.user, form.instance.email_address))
        return ret

    def get_success_url(self):
        return reverse('index')


class JoinView(FormView):
    form_class = JoinForm
    template_name = "join.html"

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_anonymous():
            _action_logger.warning('%s tried /join while signed in' %
                                   self.request.user)
            raise Http404
        return super().dispatch(*args, **kwargs)

    def get_invitation(self):
        invitation = Invitation.objects.get(
            invitation_key=self.kwargs['invitation_key'])
        if not invitation.is_valid or invitation.expires_on < timezone.now():
            raise Http404
        return invitation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['invitation'] = self.get_invitation()
        return context

    def form_valid(self, form):
        invitation = self.get_invitation()
        invitation.is_valid = False
        invitation.save()

        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            password=form.cleaned_data['password'],
            email=invitation.email_address)
        user.save()

        everyone_group, _ = Group.objects.get_or_create(name='everyone')
        user.groups.add(everyone_group)

        _action_logger.info('%s joined' % user)
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('index')
