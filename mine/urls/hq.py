from django.urls import path

from ..views.hq import (
    MineMinerDataListView,
    miner_data_detail,
    statistic_detail,
    local_worker_detail,
    foreign_worker_detail,
    machinery_detail,
    energy_supply_detail,
    operating_record_detail,
)

app_name = 'hq'

urlpatterns = [
    path('data-list/', MineMinerDataListView.as_view(), name='data_list'),
    path(
        'miner-data/<int:pk>/',
        miner_data_detail,
        name='miner_data',
    ),
    path(
        'miner-data/<int:pk>/statistic/',
        statistic_detail,
        name='statistic'
    ),
    path(
        'miner-data/<int:pk>/local-worker/',
        local_worker_detail,
        name='local_worker'
    ),
    path(
        'miner-data/<int:pk>/foreign-worker/',
        foreign_worker_detail,
        name='foreign_worker'
    ),
    path(
        'miner-data/<int:pk>/machinery/',
        machinery_detail,
        name='machinery'
    ),
    path(
        'miner-data/<int:pk>/energy-supply/',
        energy_supply_detail,
        name='energy_supply'
    ),
    path(
        'miner-data/<int:pk>/operating-record/',
        operating_record_detail,
        name='operating_record'
    ),
]
