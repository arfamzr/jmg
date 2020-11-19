from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
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
        labels = {
            "username": "Nama Pengguna",
            "first_name": "Nama Pertama",
            "last_name": "Nama Akhir",
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'state', 'image']
        labels = {
            "ic_number": "No Kad Pengenalan",
            "address1": "Alamat (No Rumah, Nama Jalan)",
            "address2": "Alamat (Daerah)",
            "address3": "Alamat (Poskod, Negeri)",
        }


class StateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['state']


class PasswordResetForm(forms.Form):
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

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
