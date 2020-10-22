from django import forms

from account.models import Profile
from quarry.models import YEAR_CHOICES, current_year, QuarryMinerData, Quarry


def get_type_of_rock():
    TYPE_OF_ROCK = list(Quarry.TYPES_OF_ROCK)
    TYPE_OF_ROCK.insert(0, (None, '------'))
    return TYPE_OF_ROCK


class ReportForm(forms.Form):
    year = forms.ChoiceField(
        label='Tahun', choices=YEAR_CHOICES, initial=current_year)
    month = forms.ChoiceField(
        label='Bulan', choices=QuarryMinerData.MONTH_CHOICES, required=False)
    rock_type = forms.ChoiceField(
        label='Jenis Batuan', choices=Quarry.TYPES_OF_ROCK, required=False)
    # state = forms.ChoiceField(
    #     label='Negeri', choices=Profile.STATE_CHOICES, required=False)


class GraphForm(forms.Form):
    year = forms.ChoiceField(
        label='Tahun', choices=YEAR_CHOICES, initial=current_year)
    rock_type1 = forms.ChoiceField(
        label='Jenis Batuan 1', choices=Quarry.TYPES_OF_ROCK)
    rock_type2 = forms.ChoiceField(
        label='Jenis Batuan 2', choices=get_type_of_rock(), required=False)
    rock_type3 = forms.ChoiceField(
        label='Jenis Batuan 3', choices=get_type_of_rock(), required=False)
    rock_type4 = forms.ChoiceField(
        label='Jenis Batuan 4', choices=get_type_of_rock(), required=False)
    rock_type5 = forms.ChoiceField(
        label='Jenis Batuan 5', choices=get_type_of_rock(), required=False)

    def clean(self):
        cleaned_data = super().clean()
        rock1 = cleaned_data.get('rock_type1')
        rock_list = [rock1]
        rock2 = cleaned_data.get('rock_type2')
        if rock2:
            rock_list.append(rock2)
        rock3 = cleaned_data.get('rock_type3')
        if rock3:
            rock_list.append(rock3)
        rock4 = cleaned_data.get('rock_type4')
        if rock4:
            rock_list.append(rock4)
        rock5 = cleaned_data.get('rock_type5')
        if rock5:
            rock_list.append(rock5)
        if len(rock_list) > len(set(rock_list)):
            raise forms.ValidationError('The rock must be unique')
        return cleaned_data
