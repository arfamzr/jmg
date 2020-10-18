from django import forms

from account.models import Profile
from quarry.models import YEAR_CHOICES, current_year, QuarryMinerData, Quarry


class ReportForm(forms.Form):
    year = forms.ChoiceField(
        label='Tahun', choices=YEAR_CHOICES, initial=current_year)
    month = forms.ChoiceField(
        label='Bulan', choices=QuarryMinerData.MONTH_CHOICES, required=False)
    rock_type = forms.ChoiceField(
        label='Jenis Batuan', choices=Quarry.TYPES_OF_ROCK, required=False)
    # state = forms.ChoiceField(
    #     label='Negeri', choices=Profile.STATE_CHOICES, required=False)
