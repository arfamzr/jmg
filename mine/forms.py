from django import forms

from .models import (
    Mine,
    Statistic,
    LocalOperator,
    LocalContractor,
    ForeignOperator,
    ForeignContractor,
    InternalCombustionMachinery,
    ElectricMachinery,
    EnergySupply,
    OperatingRecord,
)


class MineForm(forms.ModelForm):

    class Meta:
        model = Mine
        exclude = ['user']


class StatisticForm(forms.ModelForm):

    class Meta:
        model = Statistic
        exclude = ['mine']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''


class LocalOperatorForm(forms.ModelForm):

    class Meta:
        model = LocalOperator
        exclude = ['mine']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''


class LocalContractorForm(forms.ModelForm):

    class Meta:
        model = LocalContractor
        exclude = ['mine']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''


class ForeignOperatorForm(forms.ModelForm):

    class Meta:
        model = ForeignOperator
        exclude = ['mine']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''


class ForeignContractorForm(forms.ModelForm):

    class Meta:
        model = ForeignContractor
        exclude = ['mine']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''


class InternalCombustionMachineryForm(forms.ModelForm):

    class Meta:
        model = InternalCombustionMachinery
        exclude = ['mine']
        widgets = {
            'state_other': forms.Textarea(attrs={'rows': 2})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''


class ElectricMachineryForm(forms.ModelForm):

    class Meta:
        model = ElectricMachinery
        exclude = ['mine']
        widgets = {
            'state_other': forms.Textarea(attrs={'rows': 2})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''


class EnergySupplyForm(forms.ModelForm):

    class Meta:
        model = EnergySupply
        exclude = ['mine']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''


class OperatingRecordForm(forms.ModelForm):

    class Meta:
        model = OperatingRecord
        exclude = ['mine']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''
