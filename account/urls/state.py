from django.urls import path

from ..views.state import (
    UserListView,
    user_detail,
)

app_name = 'state'

urlpatterns = [
    path('user/', UserListView.as_view(), name='user_list'),
    path('user/<int:pk>/', user_detail, name='user_detail'),
]
