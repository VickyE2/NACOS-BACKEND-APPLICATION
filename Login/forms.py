from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

import re

from Login.models import BaseUser


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'mynameis_lil', 'id': 'username'})
        # That is username is used when styling. when styling the css the id should
        # be (#)username same for the remaining fields
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

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            self.add_error('username', "username can't be empty.")
        if not BaseUser.objects.filter(username=username).exists():
            self.add_error('username', "username does not exist")
        return username

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and BaseUser.objects.filter(username=username).exists():
            # Add more logic here to verify the password if necessary.
            if len(password) < 8:
                self.add_error('password', "Password must be at least 8 characters long.")
            if not re.search(r"\d", password):
                self.add_error('password', "Password must contain at least one number.")
            if not re.search(r"[!@#$%^&*()_+={}\[\]:;\"'<>?,./]", password):
                self.add_error('password', "Password must contain at least one special character.")
        else:
            self.add_error('username', "username does not exist")
        return password


class RegistrationForm(UserCreationForm):
        first_name = forms.CharField(
            label="Firstname",
            max_length=40,
            required=True,
            widget=forms.TextInput(attrs={'placeholder': 'First Name', 'id': 'first_name'})
        )
        last_name = forms.CharField(
            label="Lastname",
            max_length=40,
            required=True,
            widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'id': 'last_name'})
        )
        username = forms.CharField(
            label="Username",
            required=True,
            widget=forms.TextInput(attrs={'placeholder': 'Username', 'id': 'username'})
        )
        password1 = forms.CharField(
            label="Password",
            widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'id': 'password1'})
        )
        password2 = forms.CharField(
            label="Confirm Password",
            widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'id': 'password2'})
        )

        class Meta:
            model = BaseUser
            fields = ('first_name', 'username', 'last_name', 'password1', 'password2')

        def save(self, commit=True):
            user = super().save(commit=False)
            user.username = self.cleaned_data.get('username')
            user.first_name = self.cleaned_data.get('first_name')
            user.last_name = self.cleaned_data.get('last_name')
            if commit:
                user.save()
            return user

        def clean(self):
            cleaned_data = super().clean()
            password1 = cleaned_data.get("password1")
            password2 = cleaned_data.get("password2")

            if password1 and password2 and password1 != password2:
                self.add_error('password2', "Passwords do not match.")
            return cleaned_data

        def clean_username(self):
            username = self.cleaned_data.get('username')
            if BaseUser.objects.filter(username=username).exists():
                raise forms.ValidationError("Username already exists.")
            return username

        def clean_first_name(self):
            first_name = self.cleaned_data.get('first_name')
            if not first_name:
                raise forms.ValidationError("First Name can't be empty.")
            return first_name

        def clean_last_name(self):
            last_name = self.cleaned_data.get('last_name')
            if not last_name:
                raise forms.ValidationError("Last Name can't be empty.")
            return last_name

        def clean_password1(self):
            password1 = super().clean_password1()
            if len(password1) < 8:
                raise forms.ValidationError("Password must be at least 8 characters long.")
            if not re.fullmatch(r".*\d.*", password1):
                raise forms.ValidationError("Password must contain at least one number.")
            if not re.fullmatch(r".*[!@#$%^&*()_+={}\[\]:;\"'<>?,./].*", password1):
                raise forms.ValidationError("Password must contain at least one special character.")
            return password1