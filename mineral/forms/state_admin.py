from django import forms
from django.db.models import fields

from ..models import ProcessFactory, ProcessManager

from account.widgets import XDSoftDatePickerInput


class ProcessFactoryForm(forms.ModelForm):

    class Meta:
        model = ProcessFactory
        exclude = ['state', 'status']


class ProcessManagerForm(forms.ModelForm):

    class Meta:
        model = ProcessManager
        exclude = ['user']
