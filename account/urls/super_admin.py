from django.urls import path
from ..views.super_admin import (
    HqListView,
    hq_detail,
    HqRegistrationView,
    HQUpdateView,
    hq_toggle_active,
    hq_update_password,
    AdminListView,
    admin_detail,
    AdminRegistrationView,
    admin_update,
    admin_toggle_active,
    admin_update_password,
)

app_name = 'super_admin'

urlpatterns = [
    path('hq/', HqListView.as_view(), name='hq_list'),
    path('hq/<int:pk>/', hq_detail, name='hq_detail'),
    path('hq/register/', HqRegistrationView.as_view(), name='hq_register'),
    path('hq/<int:pk>/update/', HQUpdateView.as_view(), name='hq_update'),
    path('admin/', AdminListView.as_view(), name='admin_list'),
    path('admin/<int:pk>/', admin_detail, name='admin_detail'),
    path('admin/register/', AdminRegistrationView.as_view(), name='admin_register'),
    path('admin/<int:pk>/update/', admin_update, name='admin_update'),
    path(
        'hq/<int:pk>/toggle-active/',
        hq_toggle_active,
        name='hq_toggle_active',
    ),
    path(
        'admin/<int:pk>/toggle-active/',
        admin_toggle_active,
        name='admin_toggle_active',
    ),
    path('hq/<int:pk>/reset-password/',
         hq_update_password, name='hq_update_password'),
    path('admin/<int:pk>/reset-password/',
         admin_update_password, name='admin_update_password'),

]
