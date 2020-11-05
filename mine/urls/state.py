from django.urls import path

from ..views.state import (
    # mine
    # MineListView,

    # data
    DataListView,
    data_detail,

    #     mine_detail,
    #     user_mine_list,
    #     statistic_detail,
    #     local_worker_detail,
    #     foreign_worker_detail,
    #     machinery_detail,
    #     energy_supply_detail,
    #     operating_record_detail,
)

app_name = 'state'

urlpatterns = [
    # mine
    # path('', MineListView.as_view(), name='list'),

    # data
    path('data/', DataListView.as_view(), name='data_list'),
    path(
        'miner-data/<int:pk>/',
        data_detail,
        name='data_detail',
    ),


    # path('<int:pk>/detail/', mine_detail, name='detail'),
    # path('user-mine/<int:pk>/',
    #      user_mine_list, name='user_mine_list'),
    # path(
    #     'miner-data/<int:pk>/statistic/',
    #     statistic_detail,
    #     name='statistic'
    # ),
    # path(
    #     'miner-data/<int:pk>/local-worker/',
    #     local_worker_detail,
    #     name='local_worker'
    # ),
    # path(
    #     'miner-data/<int:pk>/foreign-worker/',
    #     foreign_worker_detail,
    #     name='foreign_worker'
    # ),
    # path(
    #     'miner-data/<int:pk>/machinery/',
    #     machinery_detail,
    #     name='machinery'
    # ),
    # path(
    #     'miner-data/<int:pk>/energy-supply/',
    #     energy_supply_detail,
    #     name='energy_supply'
    # ),
    # path(
    #     'miner-data/<int:pk>/operating-record/',
    #     operating_record_detail,
    #     name='operating_record'
    # ),
]
