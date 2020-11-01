from django import forms
from django.db.models import fields

from ..models import LeaseHolder, Manager, Operator, Mine, MainMineral, SideMineral


class LeaseHolderForm(forms.ModelForm):

    class Meta:
        model = LeaseHolder
        exclude = ['state', 'status']


class ManagerForm(forms.ModelForm):

    class Meta:
        model = Manager
        exclude = ['user']


class OperatorForm(forms.ModelForm):

    class Meta:
        model = Operator
        exclude = ['state', 'status']


class MineForm(forms.ModelForm):

    class Meta:
        model = Mine
        exclude = ['state', 'status', 'operators']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['lease_holder'].widget.attrs['disabled'] = True
    #     self.fields['operator'].widget.attrs['disabled'] = True


class MainMineralForm(forms.ModelForm):

    class Meta:
        model = MainMineral
        exclude = ['mine']


class SideMineralForm(forms.ModelForm):

    class Meta:
        model = SideMineral
        exclude = ['mine']
