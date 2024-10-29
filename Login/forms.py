from django.contrib.auth.forms import AuthenticationForm
from django import forms

import re

from Login.models import BaseUser


class LoginForm(AuthenticationForm):
    email = forms.CharField(
        label="Email",
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'mynameisemail@gmail.com', 'id': 'email'})
        # That is email is used when styling. when styling the css the id should
        # be (#)email same for the remaining fields
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'id': 'password'})

    )
    remember_me = forms.BooleanField(
        label="Remember me",
        required=False,
        widget=forms.CheckboxInput(attrs={'placeholder': 'Remember me', 'id': 'remember_me'})
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            self.add_error('email', "Username can't be empty.")
        if not BaseUser.objects.filter(email=email).exists():
            self.add_error('email', "Username does not exist")
            self.add_error('email', "Email already exists")
        return email

    def clean_password(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if BaseUser.email:
            self.add_error('password', "Username does not exist")
        if len(password) < 8:
            self.add_error('password', "Password must be at least 8 characters long.")
        if not re.search(r"\d", password):
            self.add_error('password', "Password must contain at least one number.")
        if not re.search(r"[!@#$%^&*()_+={}\[\]:;\"'<>?,./]", password):
            self.add_error('password', "Password must contain at least one special character.")

        return password