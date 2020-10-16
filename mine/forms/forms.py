from django import forms

from .models import (
    Mine,
    MineMiner,
    MineMinerData,
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
        exclude = ['status']


class MineMinerForm(forms.ModelForm):

    class Meta:
        model = MineMiner
        fields = ['lot_number', 'latitude', 'longitude']


class MineMinerDataForm(forms.ModelForm):

    class Meta:
        model = MineMinerData
        fields = ['month', 'year']


class StatisticForm(forms.ModelForm):

    class Meta:
        model = Statistic
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


class MineReadOnlyForm(forms.ModelForm):

    class Meta:
        model = Mine
        exclude = ['status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['readonly'] = True


class MineMinerReadOnlyForm(forms.ModelForm):

    class Meta:
        model = MineMiner
        fields = ['lot_number', 'latitude', 'longitude']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['readonly'] = True


class MineMinerDataReadOnlyForm(forms.ModelForm):

    class Meta:
        model = MineMinerData
        fields = ['month', 'year']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['readonly'] = True


class StatisticReadOnlyForm(forms.ModelForm):

    class Meta:
        model = Statistic
        exclude = ['miner_data']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''
            field.widget.attrs['readonly'] = True


class LocalOperatorReadOnlyForm(forms.ModelForm):

    class Meta:
        model = LocalOperator
        exclude = ['miner_data']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''
            field.widget.attrs['readonly'] = True


class LocalContractorReadOnlyForm(forms.ModelForm):

    class Meta:
        model = LocalContractor
        exclude = ['miner_data']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''
            field.widget.attrs['readonly'] = True


class ForeignOperatorReadOnlyForm(forms.ModelForm):

    class Meta:
        model = ForeignOperator
        exclude = ['miner_data']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''
            field.widget.attrs['readonly'] = True


class ForeignContractorReadOnlyForm(forms.ModelForm):

    class Meta:
        model = ForeignContractor
        exclude = ['miner_data']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''
            field.widget.attrs['readonly'] = True


class InternalCombustionMachineryReadOnlyForm(forms.ModelForm):

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
            field.widget.attrs['readonly'] = True


class ElectricMachineryReadOnlyForm(forms.ModelForm):

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
            field.widget.attrs['readonly'] = True


class EnergySupplyReadOnlyForm(forms.ModelForm):

    class Meta:
        model = EnergySupply
        exclude = ['miner_data']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''
            field.widget.attrs['readonly'] = True


class OperatingRecordReadOnlyForm(forms.ModelForm):

    class Meta:
        model = OperatingRecord
        exclude = ['miner_data']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''
            field.widget.attrs['readonly'] = True
