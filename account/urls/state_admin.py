from django.urls import path

from ..views.state_admin import (
    # jmg state list
    StateListView,
    # jmg state create
    StateRegistrationView,
    # jmg state update
    StateUpdateView,
    # jmg state toggle active
    state_toggle_active,
    # jmg state update state
    StateStateUpdateView,

    # UserListView,
    # UserRegistrationView,
    # StateListView,
    # StateRegistrationView,
    # user_detail,
    # UserUpdateView,
    # user_toggle_active,
    # state_update,
    # user_update_password,
)

app_name = 'state_admin'

urlpatterns = [
    # jmg state list
    path('state/', StateListView.as_view(), name='state_list'),
    # jmg state create
    path('state/register/', StateRegistrationView.as_view(), name='state_register'),
    # jmg state update
    path('state/<int:pk>/update/', StateUpdateView.as_view(), name='state_update'),
    # jmg state toggle active
    path('state/<int:pk>/toggle-active/',
         state_toggle_active, name='state_toggle_active'),
    # jmg state update state
    path('state/<int:pk>/update-state/',
         StateStateUpdateView.as_view(), name='state_update_state'),

    # path('user/', UserListView.as_view(), name='user_list'),
    # path('user/register/', UserRegistrationView.as_view(), name='user_register'),
    # path('user/<int:pk>/', user_detail, name='user_detail'),
    # path('user/<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    # path('state/<int:pk>/update/', state_update, name='state_update'),
    path('user/<int:pk>/reset-password/',
         user_update_password, name='user_update_password'),
    # path(
    #     'user/<int:pk>/toggle-active/',
    #     user_toggle_active,
    #     name='user_toggle_active',
    # ),
]
