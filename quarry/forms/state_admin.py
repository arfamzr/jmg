from django import forms

from ..models import LeaseHolder, QuarryManager, Operator, Quarry, MainRock, SideRock


class LeaseHolderForm(forms.ModelForm):

    class Meta:
        model = LeaseHolder
        exclude = ['state', 'status']


class QuarryManagerForm(forms.ModelForm):

    class Meta:
        model = QuarryManager
        exclude = ['user']


class OperatorForm(forms.ModelForm):

    class Meta:
        model = Operator
        exclude = ['state', 'status']


class QuarryOwnerForm(forms.Form):
    lease_holder = forms.CharField(label='Pemajak', max_length=255)
    manager = forms.CharField(label='Pengurus', max_length=255)
    operator = forms.CharField(label='Pengusaha', max_length=255)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['disabled'] = True


class QuarryForm(forms.ModelForm):

    class Meta:
        model = Quarry
        exclude = ['lease_holder', 'manager', 'operator', 'state', 'status']


class MainRockForm(forms.ModelForm):

    class Meta:
        model = MainRock
        exclude = ['mine']


class SideRockForm(forms.ModelForm):

    class Meta:
        model = SideRock
        exclude = ['mine']
