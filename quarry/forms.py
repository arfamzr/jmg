from django import forms

from account.widgets import XDSoftDatePickerInput

from .models import (
    Quarry,
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


class QuarryForm(forms.ModelForm):

    class Meta:
        model = Quarry
        exclude = ['user']


class ProductionStatisticForm(forms.ModelForm):

    class Meta:
        model = ProductionStatistic
        exclude = ['quarry']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''


class SalesSubmissionForm(forms.ModelForm):

    class Meta:
        model = SalesSubmission
        exclude = ['quarry']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''


class LocalFinalUsesForm(forms.ModelForm):

    class Meta:
        model = LocalFinalUses
        exclude = ['quarry']
        widgets = {
            'state_other': forms.Textarea(attrs={'rows': 2})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''


class ExportFinalUsesForm(forms.ModelForm):

    class Meta:
        model = ExportFinalUses
        exclude = ['quarry']
        widgets = {
            'state_other': forms.Textarea(attrs={'rows': 2})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''


class LocalOperatorForm(forms.ModelForm):

    class Meta:
        model = LocalOperator
        exclude = ['quarry']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''


class LocalContractorForm(forms.ModelForm):

    class Meta:
        model = LocalContractor
        exclude = ['quarry']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''


class ForeignOperatorForm(forms.ModelForm):

    class Meta:
        model = ForeignOperator
        exclude = ['quarry']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''


class ForeignContractorForm(forms.ModelForm):

    class Meta:
        model = ForeignContractor
        exclude = ['quarry']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''


class InternalCombustionMachineryForm(forms.ModelForm):

    class Meta:
        model = InternalCombustionMachinery
        exclude = ['quarry']
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
        exclude = ['quarry']
        widgets = {
            'state_other': forms.Textarea(attrs={'rows': 2})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''


class DailyExplosiveForm(forms.ModelForm):
    date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=XDSoftDatePickerInput(format='%d/%m/%Y'),
    )

    class Meta:
        model = DailyExplosive
        exclude = ['quarry']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''


class EnergySupplyForm(forms.ModelForm):

    class Meta:
        model = EnergySupply
        exclude = ['quarry']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''


class OperatingRecordForm(forms.ModelForm):

    class Meta:
        model = OperatingRecord
        exclude = ['quarry']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''


class RoyaltiesForm(forms.ModelForm):

    class Meta:
        model = Royalties
        exclude = ['quarry']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''


class OtherForm(forms.ModelForm):

    class Meta:
        model = Other
        exclude = ['quarry']
        widgets = {
            'title': forms.Textarea(attrs={'rows': 1}),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''
