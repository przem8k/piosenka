# coding=utf8
from django.conf import settings
from django.template import Context, RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import messages

from users.models import Profile
from users.forms import LoginForm, RegistrationForm


def hello(request, template='users/login.html'):
    cc = {}

    login_form = LoginForm()
    registration_form = RegistrationForm()

    if request.method == 'POST' and "login_submit" in request.POST:
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(username=login_form.cleaned_data['username'], password=login_form.cleaned_data['password'])
            login(request, user)
            messages.add_message(request, messages.SUCCESS, "Zostałeś zalogowany.")
            if 'next' in request.GET:
                return HttpResponseRedirect(request.GET['next'])
            else:
                return HttpResponseRedirect(reverse("index"))
    elif request.method == 'POST' and "registration_submit" in request.POST:
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            user_profile = registration_form.save()
            user = authenticate(username=registration_form.cleaned_data['username'], password=registration_form.cleaned_data['password1'])
            #send_registration_mail(request.LANGUAGE_CODE, registration_form.cleaned_data['email'], user_profile.activation_key)
            return registered(request)

    cc['login_form'] = login_form
    cc['registration_form'] = registration_form
    return render(request, template, Context(cc))


def registered(request):
    messages.add_message(request, messages.SUCCESS, "Dziękujęmy za rejestrację. Kliknij na link przesłany mailem aby aktywować konto.")
    return HttpResponseRedirect(reverse("index"))


def activate(request, activation_key):
    profile = get_object_or_404(Profile, activation_key=activation_key, user__is_active=False)
    profile.user.is_active = True
    profile.user.save()
    messages.add_message(request, messages.SUCCESS, "Twoje konto zostało aktywowane. Zapraszamy do zalogowania się na konto.")
    return HttpResponseRedirect(reverse("hello"))


def goodbye(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, "Zostałeś wylogowany. Dziękujemy za odwiedziny.")
    return HttpResponseRedirect(reverse("index"))
