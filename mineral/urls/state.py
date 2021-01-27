from django.urls import path

from ..views.state import (

    # data
    DataListView,
    data_detail,
)

app_name = 'state'

urlpatterns = [
    # data
    path('data/', DataListView.as_view(), name='data_list'),
    path(
        'miner-data/<int:pk>/',
        data_detail,
        name='data_detail',
    ),
]
