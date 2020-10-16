from django import forms

from ..models import Quarry, QuarryMiner


class QuarryForm(forms.ModelForm):

    class Meta:
        model = Quarry
        exclude = ['state', 'status']


class QuarryMinerForm(forms.ModelForm):

    class Meta:
        model = QuarryMiner
        fields = ['lot_number', 'latitude', 'longitude']
