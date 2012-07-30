# coding=utf8
import random
import sha

from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate

from users.models import Profile


class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=100, label="Imię")
    last_name = forms.CharField(max_length=100, label="Nazwisko")
    username = forms.CharField(max_length=30, label="Login")
    email = forms.EmailField()
    password1 = forms.CharField(max_length=30, widget=forms.PasswordInput(render_value=False), label="Hasło")
    password2 = forms.CharField(max_length=30, widget=forms.PasswordInput(render_value=False), label="Hasło (ponownie)")
    hide_real_name = forms.BooleanField(label="Ukryj imię i nazwisko")

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data['username']).count() > 0:
            raise forms.ValidationError("Ta nazwa użytkownika jest już zajęta.")
        return self.cleaned_data['username']

    def clean_email(self):
        #if User.objects.filter(email=self.cleaned_data['email']).count() > 0:
        #    raise forms.ValidationError("This email is already registered in our database. Please choose another.")
        return self.cleaned_data['email']

    def clean(self):
        if ('password1' in self.cleaned_data) and ('password2' in self.cleaned_data):
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Podane hasła nie zgadzają się.")
        return self.cleaned_data

    def save(self):
        new_user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1']
        )
        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        new_user.is_active = False

        salt = sha.new(str(random.random())).hexdigest()[:5]
        activation_key = sha.new(salt + new_user.username.encode('ascii', 'ignore')).hexdigest()
        new_profile = Profile(
            user=new_user,
            activation_key=activation_key,
            hide_real_name=self.cleaned_data['hide_real_name'],
        )

        new_user.save()
        new_profile.save()
        return new_profile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, label="Login")
    password = forms.CharField(max_length=30, widget=forms.PasswordInput(render_value=False), label="Hasło")

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user != None:
            if not user.is_active:
                raise forms.ValidationError("Konto nie zostało jeszcze aktywowane. Kliknij proszę na link potwierdzający, który przesłaliśmy mailem.")
        else:
            raise forms.ValidationError("Nieprawidłowa nazwa użytkownika lub hasło")
        return self.cleaned_data
