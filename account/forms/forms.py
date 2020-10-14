from django import forms
from django.contrib.auth import password_validation
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.forms import (
    UsernameField,
    AuthenticationForm as DjangoAuthenticationForm,
    UserCreationForm as DjangoUserCreationForm,
)

from ..models import User


class AuthenticationForm(DjangoAuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Enter Username'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'
        for field_name, field in self.fields.items():
            field.label = ''
            field.widget.attrs['class'] = 'form-control form-control-user'


class UserCreationForm(DjangoUserCreationForm):
    password1 = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'placeholder': 'Password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label='',
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
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }
        required = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': '',
            'first_name': '',
            'last_name': '',
            'email': '',
        }
        field_classes = {'username': UsernameField}
