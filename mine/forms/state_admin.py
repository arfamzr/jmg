from django import forms
from django.db.models import fields

from ..models import LeaseHolder, Manager, Operator, Mine, MainMineral, SideMineral, MineMiner


class LeaseHolderForm(forms.ModelForm):

    class Meta:
        model = LeaseHolder
        exclude = ['state', 'status']


class ManagerForm(forms.ModelForm):

    class Meta:
        model = Manager
        fields = '__all__'


class OperatorForm(forms.ModelForm):

    class Meta:
        model = Operator
        exclude = ['state', 'status']


class MineForm(forms.ModelForm):

    class Meta:
        model = Mine
        exclude = ['state', 'status', 'operators']


class MainMineralForm(forms.ModelForm):

    class Meta:
        model = MainMineral
        exclude = ['mine']


class SideMineralForm(forms.ModelForm):

    class Meta:
        model = SideMineral
        exclude = ['mine']


class MineMinerForm(forms.ModelForm):

    class Meta:
        model = MineMiner
        fields = ['lot_number', 'latitude', 'longitude']
