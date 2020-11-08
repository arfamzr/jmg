from django import forms

from account.widgets import XDSoftDatePickerInput

from ..models import (
    Data,
    MainProductionStatistic,
    SideProductionStatistic,
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


class DataForm(forms.ModelForm):

    class Meta:
        model = Data
        fields = ['month', 'year']

    def __init__(self, *args, **kwargs):
        self.manager = kwargs.pop('manager', None)
        super().__init__(*args, **kwargs)

    def clean(self, added_error=False):
        cleaned_data = super().clean()
        month = cleaned_data.get('month')
        year = cleaned_data.get('year')

        if Data.objects.filter(manager=self.manager, month=month, year=year):
            raise forms.ValidationError(
                'Data untuk bulan dan tahun tersebut telah tersedia!')

        return cleaned_data


class MainProductionStatisticForm(forms.ModelForm):

    class Meta:
        model = MainProductionStatistic
        exclude = ['data']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         field.label = ''


class SideProductionStatisticForm(forms.ModelForm):

    class Meta:
        model = SideProductionStatistic
        exclude = ['data']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         field.label = ''


class SalesSubmissionForm(forms.ModelForm):

    class Meta:
        model = SalesSubmission
        exclude = ['data']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         field.label = ''


class LocalFinalUsesForm(forms.ModelForm):

    class Meta:
        model = LocalFinalUses
        exclude = ['data']
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
        exclude = ['data']
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
        exclude = ['data']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''


class LocalContractorForm(forms.ModelForm):

    class Meta:
        model = LocalContractor
        exclude = ['data']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''


class ForeignOperatorForm(forms.ModelForm):

    class Meta:
        model = ForeignOperator
        exclude = ['data']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''


class ForeignContractorForm(forms.ModelForm):

    class Meta:
        model = ForeignContractor
        exclude = ['data']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''


class InternalCombustionMachineryForm(forms.ModelForm):

    class Meta:
        model = InternalCombustionMachinery
        exclude = ['data']
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
        exclude = ['data']
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
        exclude = ['data']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''


class EnergySupplyForm(forms.ModelForm):

    class Meta:
        model = EnergySupply
        exclude = ['data']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''


class OperatingRecordForm(forms.ModelForm):

    class Meta:
        model = OperatingRecord
        exclude = ['data']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''


class RoyaltiesForm(forms.ModelForm):

    class Meta:
        model = Royalties
        exclude = ['data']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''


class OtherForm(forms.ModelForm):

    class Meta:
        model = Other
        exclude = ['data']
        widgets = {
            'title': forms.Textarea(attrs={'rows': 1}),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''
