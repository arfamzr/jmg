from django import forms

from account.widgets import XDSoftDatePickerInput

from ..models import (
    Quarry,
    QuarryMiner,
    QuarryMinerData,
    ProductionStatistic,
    SalesSubmission,
    LocalFinalUses,
    ExportFinalUses,
    LocalOperator,
    LocalContractor,
    ForeignOperator,
    ForeignContractor,
    InternalCombustionMachinery,
    ElectricMachinery,
    DailyExplosive,
    EnergySupply,
    OperatingRecord,
    Royalties,
    Other,
)


class QuarryReadOnlyForm(forms.ModelForm):

    class Meta:
        model = Quarry
        exclude = ['status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['readonly'] = True


class QuarryMinerReadOnlyForm(forms.ModelForm):

    class Meta:
        model = QuarryMiner
        fields = ['lot_number', 'latitude', 'longitude']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['readonly'] = True


class QuarryMinerDataReadOnlyForm(forms.ModelForm):

    class Meta:
        model = QuarryMinerData
        fields = ['month', 'year']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['readonly'] = True


class ProductionStatisticReadOnlyForm(forms.ModelForm):

    class Meta:
        model = ProductionStatistic
        exclude = ['miner_data']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''
            field.widget.attrs['readonly'] = True


class SalesSubmissionReadOnlyForm(forms.ModelForm):

    class Meta:
        model = SalesSubmission
        exclude = ['miner_data']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''
            field.widget.attrs['readonly'] = True


class LocalFinalUsesReadOnlyForm(forms.ModelForm):

    class Meta:
        model = LocalFinalUses
        exclude = ['miner_data']
        widgets = {
            'state_other': forms.Textarea(attrs={'rows': 2})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''
            field.widget.attrs['readonly'] = True


class ExportFinalUsesReadOnlyForm(forms.ModelForm):

    class Meta:
        model = ExportFinalUses
        exclude = ['miner_data']
        widgets = {
            'state_other': forms.Textarea(attrs={'rows': 2})
        }

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


class DailyExplosiveReadOnlyForm(forms.ModelForm):
    date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=XDSoftDatePickerInput(format='%d/%m/%Y'),
    )

    class Meta:
        model = DailyExplosive
        exclude = ['miner_data']

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


class RoyaltiesReadOnlyForm(forms.ModelForm):

    class Meta:
        model = Royalties
        exclude = ['miner_data']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''
            field.widget.attrs['readonly'] = True


class OtherReadOnlyForm(forms.ModelForm):

    class Meta:
        model = Other
        exclude = ['miner_data']
        widgets = {
            'title': forms.Textarea(attrs={'rows': 1}),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''
            field.widget.attrs['readonly'] = True
