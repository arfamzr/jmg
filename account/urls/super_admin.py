from django.urls import path
from ..views.super_admin import (
    # hq list
    HQListView,
    # hq create
    HQRegistrationView,
    # hq update
    HQUpdateView,
    # hq toggle active
    hq_toggle_active,

    # state admin list
    AdminListView,
    # state admin create
    AdminRegistrationView,
    # state admin update
    AdminUpdateView,
    # state admin toggle active
    state_admin_toggle_active,
    # state admin update state
    AdminStateUpdateView,

    # HqListView,
    # hq_detail,
    # HqRegistrationView,
    # HQUpdateView,
    # hq_toggle_active,
    # hq_update_password,
    # AdminListView,
    # admin_detail,
    # AdminRegistrationView,
    # admin_update,
    # admin_toggle_active,
    # admin_update_password,
)

app_name = 'super_admin'

urlpatterns = [
    # hq list
    path('hq/', HQListView.as_view(), name='hq_list'),
    # hq create
    path('hq/register/', HQRegistrationView.as_view(), name='hq_register'),
    # hq update
    path('hq/<int:pk>/update/', HQUpdateView.as_view(), name='hq_update'),
    # hq toggle active
    path('hq/<int:pk>/toggle-active/',
         hq_toggle_active, name='hq_toggle_active'),

    # state admin list
    path('state-admin/', AdminListView.as_view(), name='state_admin_list'),
    # state admin create
    path('state-admin/register/', AdminRegistrationView.as_view(),
         name='state_admin_register'),
    # state admin update
    path('state-admin/<int:pk>/update/',
         AdminUpdateView.as_view(), name='state_admin_update'),
    # state admin toggle active
    path('state-admin/<int:pk>/toggle-active/',
         state_admin_toggle_active, name='state_admin_toggle_active'),
    # state admin update state
    path('state-admin/<int:pk>/update-state/',
         AdminStateUpdateView.as_view(), name='state_admin_update_state'),

    # path('hq/', HqListView.as_view(), name='hq_list'),
    # path('hq/<int:pk>/', hq_detail, name='hq_detail'),
    # path('hq/register/', HqRegistrationView.as_view(), name='hq_register'),
    # path('hq/<int:pk>/update/', HQUpdateView.as_view(), name='hq_update'),
    # path('admin/', AdminListView.as_view(), name='admin_list'),
    # path('admin/<int:pk>/', admin_detail, name='admin_detail'),
    # path('admin/register/', AdminRegistrationView.as_view(), name='admin_register'),
    # path('admin/<int:pk>/update/', admin_update, name='admin_update'),
    # path(
    #     'hq/<int:pk>/toggle-active/',
    #     hq_toggle_active,
    #     name='hq_toggle_active',
    # ),
    # path(
    #     'admin/<int:pk>/toggle-active/',
    #     admin_toggle_active,
    #     name='admin_toggle_active',
    # ),
    # path('hq/<int:pk>/reset-password/',
    #      hq_update_password, name='hq_update_password'),
    # path('admin/<int:pk>/reset-password/',
    #      admin_update_password, name='admin_update_password'),

]
