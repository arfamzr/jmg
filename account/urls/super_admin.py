from django.urls import path
from ..views.super_admin import (
    HqListView,
    hq_detail,
    HqRegistrationView,
    AdminListView,
    admin_detail,
    AdminRegistrationView,
)

app_name = 'super_admin'

urlpatterns = [
    path('hq/', HqListView.as_view(), name='hq_list'),
    path('hq/<int:pk>/', hq_detail, name='hq_detail'),
    path('hq/register/', HqRegistrationView.as_view(), name='hq_register'),
    path('admin/', AdminListView.as_view(), name='admin_list'),
    path('admin/<int:pk>/', admin_detail, name='admin_detail'),
    path('admin/register/', AdminRegistrationView.as_view(), name='admin_register'),

]
