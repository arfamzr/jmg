from django.urls import path

from ..views.state import (
    MineListView,
    mine_detail,
    user_mine_list,
    QuarryMinerDataListView,
    miner_data_detail,
    statistic_detail,
    local_worker_detail,
    foreign_worker_detail,
    machinery_detail,
    energy_supply_detail,
    operating_record_detail,
)

app_name = 'state'

urlpatterns = [
    path('', MineListView.as_view(), name='list'),
    path('<int:pk>/detail/', mine_detail, name='detail'),
    path('user-mine/<int:pk>/',
         user_mine_list, name='user_mine_list'),
    path('data-list/', QuarryMinerDataListView.as_view(), name='data_list'),
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
