from django import forms

from quarry.models import YEAR_CHOICES, current_year, Data, Choices as RockChoices
from mine.models import Choices as MineralChoices


def get_type_of_rock():
    TYPE_OF_ROCK = list(RockChoices.TYPES_OF_ROCK)
    TYPE_OF_ROCK.insert(0, (None, '------'))
    return TYPE_OF_ROCK


def get_type_of_mineral():
    TYPE_OF_MINERAL = list(MineralChoices.TYPES_OF_MINERAL)
    TYPE_OF_MINERAL.insert(0, (None, '------'))
    return TYPE_OF_MINERAL


def get_month_choices():
    MONTH_CHOICES = list(Data.MONTH_CHOICES)
    MONTH_CHOICES.insert(0, (None, '------'))
    return MONTH_CHOICES


class GraphForm(forms.Form):
    year = forms.ChoiceField(
        label='Tahun', choices=YEAR_CHOICES, initial=current_year)
    month = forms.ChoiceField(
        label='Bulan', choices=get_month_choices(), required=False)
    rock_type1 = forms.ChoiceField(
        label='Jenis Batuan 1', choices=RockChoices.TYPES_OF_ROCK)
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


# quarry production graph
class QuarryProductionGraphForm(forms.Form):
    year = forms.ChoiceField(
        label='Tahun', choices=YEAR_CHOICES, initial=current_year)
    month = forms.ChoiceField(
        label='Bulan', choices=get_month_choices(), required=False)
    main_rock_type1 = forms.ChoiceField(
        label='Jenis Batuan Utama 1', choices=RockChoices.TYPES_OF_ROCK)
    main_rock_type2 = forms.ChoiceField(
        label='Jenis Batuan Utama 2', choices=get_type_of_rock(), required=False)
    main_rock_type3 = forms.ChoiceField(
        label='Jenis Batuan Utama 3', choices=get_type_of_rock(), required=False)
    main_rock_type4 = forms.ChoiceField(
        label='Jenis Batuan Utama 4', choices=get_type_of_rock(), required=False)
    main_rock_type5 = forms.ChoiceField(
        label='Jenis Batuan Utama 5', choices=get_type_of_rock(), required=False)
    side_rock_type1 = forms.ChoiceField(
        label='Jenis Batuan Sampingan 1', choices=get_type_of_rock(), required=False)
    side_rock_type2 = forms.ChoiceField(
        label='Jenis Batuan Sampingan 2', choices=get_type_of_rock(), required=False)
    side_rock_type3 = forms.ChoiceField(
        label='Jenis Batuan Sampingan 3', choices=get_type_of_rock(), required=False)
    side_rock_type4 = forms.ChoiceField(
        label='Jenis Batuan Sampingan 4', choices=get_type_of_rock(), required=False)
    side_rock_type5 = forms.ChoiceField(
        label='Jenis Batuan Sampingan 5', choices=get_type_of_rock(), required=False)

    def clean(self):
        cleaned_data = super().clean()
        main_rock1 = cleaned_data.get('main_rock_type1')
        main_rock_list = [main_rock1]
        main_rock2 = cleaned_data.get('main_rock_type2')
        if main_rock2:
            main_rock_list.append(main_rock2)
        main_rock3 = cleaned_data.get('main_rock_type3')
        if main_rock3:
            main_rock_list.append(main_rock3)
        main_rock4 = cleaned_data.get('main_rock_type4')
        if main_rock4:
            main_rock_list.append(main_rock4)
        main_rock5 = cleaned_data.get('main_rock_type5')
        if main_rock5:
            main_rock_list.append(main_rock5)
        if len(main_rock_list) > len(set(main_rock_list)):
            raise forms.ValidationError('The main rock must be unique')

        side_rock1 = cleaned_data.get('side_rock_type1')
        side_rock_list = [side_rock1]
        side_rock2 = cleaned_data.get('side_rock_type2')
        if side_rock2:
            side_rock_list.append(side_rock2)
        side_rock3 = cleaned_data.get('side_rock_type3')
        if side_rock3:
            side_rock_list.append(side_rock3)
        side_rock4 = cleaned_data.get('side_rock_type4')
        if side_rock4:
            side_rock_list.append(side_rock4)
        side_rock5 = cleaned_data.get('side_rock_type5')
        if side_rock5:
            side_rock_list.append(side_rock5)
        if len(side_rock_list) > len(set(side_rock_list)):
            raise forms.ValidationError('The side rock must be unique')
        return cleaned_data


# mine production graph
class MineProductionGraphForm(forms.Form):
    year = forms.ChoiceField(
        label='Tahun', choices=YEAR_CHOICES, initial=current_year)
    month = forms.ChoiceField(
        label='Bulan', choices=get_month_choices(), required=False)
    main_rock_type1 = forms.ChoiceField(
        label='Jenis Mineral Utama 1', choices=MineralChoices.TYPES_OF_MINERAL)
    main_rock_type2 = forms.ChoiceField(
        label='Jenis Mineral Utama 2', choices=get_type_of_mineral(), required=False)
    main_rock_type3 = forms.ChoiceField(
        label='Jenis Mineral Utama 3', choices=get_type_of_mineral(), required=False)
    main_rock_type4 = forms.ChoiceField(
        label='Jenis Mineral Utama 4', choices=get_type_of_mineral(), required=False)
    main_rock_type5 = forms.ChoiceField(
        label='Jenis Mineral Utama 5', choices=get_type_of_mineral(), required=False)
    side_rock_type1 = forms.ChoiceField(
        label='Jenis Mineral Sampingan 1', choices=get_type_of_mineral(), required=False)
    side_rock_type2 = forms.ChoiceField(
        label='Jenis Mineral Sampingan 2', choices=get_type_of_mineral(), required=False)
    side_rock_type3 = forms.ChoiceField(
        label='Jenis Mineral Sampingan 3', choices=get_type_of_mineral(), required=False)
    side_rock_type4 = forms.ChoiceField(
        label='Jenis Mineral Sampingan 4', choices=get_type_of_mineral(), required=False)
    side_rock_type5 = forms.ChoiceField(
        label='Jenis Mineral Sampingan 5', choices=get_type_of_mineral(), required=False)

    def clean(self):
        cleaned_data = super().clean()
        main_rock1 = cleaned_data.get('main_rock_type1')
        main_rock_list = [main_rock1]
        main_rock2 = cleaned_data.get('main_rock_type2')
        if main_rock2:
            main_rock_list.append(main_rock2)
        main_rock3 = cleaned_data.get('main_rock_type3')
        if main_rock3:
            main_rock_list.append(main_rock3)
        main_rock4 = cleaned_data.get('main_rock_type4')
        if main_rock4:
            main_rock_list.append(main_rock4)
        main_rock5 = cleaned_data.get('main_rock_type5')
        if main_rock5:
            main_rock_list.append(main_rock5)
        if len(main_rock_list) > len(set(main_rock_list)):
            raise forms.ValidationError('The main mineral must be unique')

        side_rock1 = cleaned_data.get('side_rock_type1')
        side_rock_list = [side_rock1]
        side_rock2 = cleaned_data.get('side_rock_type2')
        if side_rock2:
            side_rock_list.append(side_rock2)
        side_rock3 = cleaned_data.get('side_rock_type3')
        if side_rock3:
            side_rock_list.append(side_rock3)
        side_rock4 = cleaned_data.get('side_rock_type4')
        if side_rock4:
            side_rock_list.append(side_rock4)
        side_rock5 = cleaned_data.get('side_rock_type5')
        if side_rock5:
            side_rock_list.append(side_rock5)
        if len(side_rock_list) > len(set(side_rock_list)):
            raise forms.ValidationError('The side mineral must be unique')
        return cleaned_data


# mine woker graph
class MineWorkerGraphForm(forms.Form):
    year = forms.ChoiceField(
        label='Tahun', choices=YEAR_CHOICES, initial=current_year)
    month = forms.ChoiceField(
        label='Bulan', choices=get_month_choices(), required=False)
    rock_type1 = forms.ChoiceField(
        label='Jenis mineral 1', choices=MineralChoices.TYPES_OF_MINERAL)
    rock_type2 = forms.ChoiceField(
        label='Jenis mineral 2', choices=get_type_of_mineral(), required=False)
    rock_type3 = forms.ChoiceField(
        label='Jenis mineral 3', choices=get_type_of_mineral(), required=False)
    rock_type4 = forms.ChoiceField(
        label='Jenis mineral 4', choices=get_type_of_mineral(), required=False)
    rock_type5 = forms.ChoiceField(
        label='Jenis mineral 5', choices=get_type_of_mineral(), required=False)

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
            raise forms.ValidationError('The mineral must be unique')
        return cleaned_data
