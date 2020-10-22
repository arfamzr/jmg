from django.urls import path
from ..views.super_admin import (
    HqListView,
    HqRegistrationView,
    AdminListView,
    AdminRegistrationView,
)

app_name = 'super_admin'

urlpatterns = [
    path('hq/', HqListView.as_view(), name='hq_list'),
    path('hq/register/', HqRegistrationView.as_view(), name='hq_register'),
    path('admin/', AdminListView.as_view(), name='admin_list'),
    path('admin/register/', AdminRegistrationView.as_view(), name='admin_register'),
]
