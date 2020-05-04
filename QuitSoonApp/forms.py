import unicodedata

from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext, gettext_lazy as _


class RegistrationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given username, email and
    password.
    """
    email = forms.EmailField(required=True)

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("This email already used")
        return data

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user