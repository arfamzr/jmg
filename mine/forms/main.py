from django import forms

from ..models import (
    MineMinerData,
    MainStatistic,
    SideStatistic,
    LocalOperator,
    LocalContractor,
    ForeignOperator,
    ForeignContractor,
    InternalCombustionMachinery,
    ElectricMachinery,
    EnergySupply,
    OperatingRecord,
)


class MineMinerDataForm(forms.ModelForm):

    class Meta:
        model = MineMinerData
        fields = ['month', 'year']


class MainStatisticForm(forms.ModelForm):

    class Meta:
        model = MainStatistic
        exclude = ['miner_data']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''


class SideStatisticForm(forms.ModelForm):

    class Meta:
        model = SideStatistic
        exclude = ['miner_data']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''


class LocalOperatorForm(forms.ModelForm):

    class Meta:
        model = LocalOperator
        exclude = ['miner_data']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''


class LocalContractorForm(forms.ModelForm):

    class Meta:
        model = LocalContractor
        exclude = ['miner_data']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''


class ForeignOperatorForm(forms.ModelForm):

    class Meta:
        model = ForeignOperator
        exclude = ['miner_data']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''


class ForeignContractorForm(forms.ModelForm):

    class Meta:
        model = ForeignContractor
        exclude = ['miner_data']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''


class InternalCombustionMachineryForm(forms.ModelForm):

    class Meta:
        model = InternalCombustionMachinery
        exclude = ['miner_data']
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
        exclude = ['miner_data']
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
        exclude = ['miner_data']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''


class OperatingRecordForm(forms.ModelForm):

    class Meta:
        model = OperatingRecord
        exclude = ['miner_data']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''
