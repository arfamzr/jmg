from django.urls import path

from ..views.state_admin import (
    UserListView,
    UserRegistrationView,
    user_detail,
    UserUpdateView,
    user_toggle_active,
)

app_name = 'state_admin'

urlpatterns = [
    path('user/', UserListView.as_view(), name='user_list'),
    path('user/register/', UserRegistrationView.as_view(), name='user_register'),
    path('user/<int:pk>/', user_detail, name='user_detail'),
    path('user/<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path(
        'user/<int:pk>/toggle-active/',
        user_toggle_active,
        name='user_toggle_active',
    ),
]
