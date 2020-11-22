from django import forms
from django.contrib.auth import password_validation
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.forms import (
    UsernameField,
    AuthenticationForm as DjangoAuthenticationForm,
    UserCreationForm as DjangoUserCreationForm,
    PasswordChangeForm as DjangoPasswordChangeForm,
)

from ..models import User


class AuthenticationForm(DjangoAuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Masukkan Nama Pengguna'
        self.fields['password'].widget.attrs['placeholder'] = 'Kata Laluan'
        for field_name, field in self.fields.items():
            field.label = ''
            field.widget.attrs['class'] = 'form-control form-control-user'


class UserCreationForm(DjangoUserCreationForm):
    password1 = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'placeholder': 'Kata Laluan'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'placeholder': 'Ulang Kata Laluan'}),
        strip=False,
        help_text=_(
            "Masukkan kata laluan yang sama seperti sebelumnya, untuk pengesahan."),
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


class PasswordChangeForm(DjangoPasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = "Kata laluan lama"
        self.fields['new_password1'].label = "Kata laluan baru"
        self.fields['new_password2'].label = "Pengesahan kata laluan baru"
