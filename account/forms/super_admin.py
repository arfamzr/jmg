from .state_admin import UserCreationForm

from account.models import Profile

class HqUserCreationForm(UserCreationForm):
    state = forms.ChoiceField(
        label='Negeri', choices=Profile.STATE_CHOICES, required=False)