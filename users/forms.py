# coding: utf-8
from django import forms
from django.contrib.auth.models import User


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class SignInForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')
