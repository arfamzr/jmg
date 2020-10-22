from django import forms
from django.contrib.auth import password_validation
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.forms import (
    UsernameField,
    AuthenticationForm as DjangoAuthenticationForm,
    UserCreationForm as DjangoUserCreationForm,
)

from ..models import User, Profile


class UserCreationForm(DjangoUserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'placeholder': 'Password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'placeholder': 'Password Confirmation'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        required = ['username', 'email', 'first_name', 'last_name']
        field_classes = {'username': UsernameField}


class UserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        required = ['username', 'email', 'first_name', 'last_name']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['state']
