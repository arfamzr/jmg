from django import forms
from django.contrib.auth import password_validation
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.forms import (
    UsernameField,
    AuthenticationForm as DjangoAuthenticationForm,
    UserCreationForm as DjangoUserCreationForm,
)


class AuthenticationForm(DjangoAuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Enter Username'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'
        for field_name, field in self.fields.items():
            field.label = ''
            field.widget.attrs['class'] = 'form-control form-control-user'
