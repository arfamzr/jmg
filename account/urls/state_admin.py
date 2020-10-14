from django.urls import path

from ..views.state_admin import (
    UserListView,
    UserRegistrationView,
    user_detail,
    UserUpdateView,
    user_toggle_active,
    add_company,
    remove_company,
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
    path(
        'user/<int:user_pk>/add-company/<int:company_pk>/',
        add_company,
        name='add_company',
    ),
    path(
        'user/<int:pk>/remove-company/',
        remove_company,
        name='remove_company',
    ),
]
