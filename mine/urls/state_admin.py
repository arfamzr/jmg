from django.urls import path

from ..views.state_admin import (
    MineListView,
    MineCreateView,
    MineUpdateView,
    mine_detail,
    add_miner,
    mine_add_miner,
    mine_remove_miner,
    toggle_active,
    user_mine_list,
    MineMinerDataListView,
    miner_data_detail,
    statistic_detail,
    local_worker_detail,
    foreign_worker_detail,
    machinery_detail,
    energy_supply_detail,
    operating_record_detail,
)

app_name = 'state_admin'

urlpatterns = [
    path('', MineListView.as_view(), name='list'),
    path('create/', MineCreateView.as_view(), name='create'),
    path('<int:pk>/update/', MineUpdateView.as_view(), name='update'),
    path('<int:pk>/detail/', mine_detail, name='detail'),
    path('<int:pk>/toggle-active/', toggle_active, name='toggle_active'),
    path('<int:pk>/add-miner/', add_miner, name='add_miner'),
    path('<int:mine_pk>/add-miner/<int:user_pk>/',
         mine_add_miner, name='mine_add_miner'),
    path('remove-miner/<int:pk>/',
         mine_remove_miner, name='mine_remove_miner'),
    path('user-mine/<int:pk>/',
         user_mine_list, name='user_mine_list'),
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
