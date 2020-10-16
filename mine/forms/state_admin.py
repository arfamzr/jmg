from django import forms

from ..models import Mine, MineMiner


class MineForm(forms.ModelForm):

    class Meta:
        model = Mine
        exclude = ['state', 'status']


class MineMinerForm(forms.ModelForm):

    class Meta:
        model = MineMiner
        fields = ['lot_number', 'latitude', 'longitude']
