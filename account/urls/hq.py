from django.urls import path

from ..views.hq import (
    # state admin list
    AdminListView,

    # state list
    StateListView,
)

app_name = 'hq'

urlpatterns = [
    # state admin list
    path('state-admin/', AdminListView.as_view(), name='state_admin_list'),

    # state list
    path('state/', StateListView.as_view(), name='state_list'),
]
