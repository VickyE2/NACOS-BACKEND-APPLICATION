from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
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
            self.add_error('email', "Email can't be empty.")
        if not BaseUser.objects.filter(email=email).exists():
            self.add_error('email', "Email does not exist")
        return email

    def clean_password(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and BaseUser.objects.filter(email=email).exists():
            # Add more logic here to verify the password if necessary.
            if len(password) < 8:
                self.add_error('password', "Password must be at least 8 characters long.")
            if not re.search(r"\d", password):
                self.add_error('password', "Password must contain at least one number.")
            if not re.search(r"[!@#$%^&*()_+={}\[\]:;\"'<>?,./]", password):
                self.add_error('password', "Password must contain at least one special character.")
        else:
            self.add_error('email', "Email does not exist")
        return password


class RegistrationForm(UserCreationForm):
        first_name = forms.CharField(
            max_length=40,
            required=True,
            widget=forms.TextInput(attrs={'placeholder': 'First Name', 'id': 'first_name'})
        )
        last_name = forms.CharField(
            max_length=40,
            required=True,
            widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'id': 'last_name'})
        )
        email = forms.EmailField(
            required=True,
            widget=forms.EmailInput(attrs={'placeholder': 'Email', 'id': 'email'})
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
            fields = ('first_name', 'email', 'last_name', 'password1', 'password2')

        def save(self, commit=True):
            user = super().save(commit=False)
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            if commit:
                user.save()
            return user

        def clean(self):
            cleaned_data = super().clean()
            password1 = cleaned_data.get("password1")
            password2 = cleaned_data.get("password2")

            # Check if passwords match
            if password1 and password2 and password1 != password2:
                self.add_error('password2', "Passwords do not match.")

            return cleaned_data

        def clean_email(self):
            email = self.cleaned_data['email']
            if BaseUser.objects.filter(email=email).exists():
                raise forms.ValidationError("Email already exists")
            return email

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
            password1 = self.cleaned_data.get('password1')
            if len(password1) < 8:
                raise forms.ValidationError("Password must be at least 8 characters long.")
            if not re.search(r"\d", password1):
                raise forms.ValidationError("Password must contain at least one number.")
            if not re.search(r"[!@#$%^&*()_+={}\[\]:;\"'<>?,./]", password1):
                raise forms.ValidationError("Password must contain at least one special character.")