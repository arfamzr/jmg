from django import forms
from django.db.models import fields

from ..models import LeaseHolder, MineManager, Operator, Mine, MainMineral, SideMineral

from account.widgets import XDSoftDatePickerInput


class LeaseHolderForm(forms.ModelForm):
    lease_expired = forms.DateField(
        label='Tarikh Tamat Pajakan',
        input_formats=['%d/%m/%Y'],
        widget=XDSoftDatePickerInput(format='%d/%m/%Y'),
    )

    class Meta:
        model = LeaseHolder
        exclude = ['state', 'status']


class MineManagerForm(forms.ModelForm):

    class Meta:
        model = MineManager
        exclude = ['user']


class OperatorForm(forms.ModelForm):

    class Meta:
        model = Operator
        exclude = ['state', 'status']


class MineOwnerForm(forms.Form):
    lease_holder = forms.CharField(label='Pemajak', max_length=255)
    manager = forms.CharField(label='Pengurus', max_length=255)
    operator = forms.CharField(label='Pengusaha', max_length=255)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['disabled'] = True


class MineForm(forms.ModelForm):

    class Meta:
        model = Mine
        exclude = ['lease_holder', 'manager', 'operator', 'state', 'status']

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
