from crispy_forms.layout import Div
from django import forms
from django.forms import formsets
from django.forms.models import formset_factory, modelformset_factory
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.bootstrap import Div

from account.widgets import XDSoftDatePickerInput

from ..models import (
    ProcessData,
    ProcessStatistic,
    ProcessSubmission,
    LocalOperator,
    LocalContractor,
    ForeignOperator,
    ForeignContractor,
    InternalCombustionMachinery,
    ElectricMachinery,
    EnergySupply,
    OperatingRecord,
    Other,
)


class DataForm(forms.ModelForm):
    class Meta:
        model = ProcessData
        fields = ['month', 'year']

    def __init__(self, *args, **kwargs):
        self.manager = kwargs.pop('manager', None)
        super().__init__(*args, **kwargs)

    def clean(self, added_error=False):
        cleaned_data = super().clean()
        month = cleaned_data.get('month')
        year = cleaned_data.get('year')

        if ProcessData.objects.filter(manager=self.manager, month=month, year=year):
            raise forms.ValidationError(
                'Data untuk bulan dan tahun tersebut telah tersedia!')

        return cleaned_data


class ProcessStatisticForm(forms.ModelForm):

    class Meta:
        model = ProcessStatistic
        exclude = ['data']


class ProcessSubmissionForm(forms.ModelForm):

    class Meta:
        model = ProcessSubmission
        exclude = ['data']


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
