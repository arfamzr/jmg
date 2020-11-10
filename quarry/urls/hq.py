from django.urls import path

from ..views.hq import (
    # data
    DataSuccessListView,
    data_success_detail,

    # QuarryMinerDataListView,
    # miner_data_detail,
    # production_statistic_detail,
    # sales_submission_detail,
    # final_uses_detail,
    # local_worker_detail,
    # foreign_worker_detail,
    # machinery_detail,
    # daily_explosive_detail,
    # energy_supply_detail,
    # operating_record_detail,
    # royalties_detail,
    # other_detail,
)

app_name = 'hq'

urlpatterns = [
    # data
    path('data-list/success/', DataSuccessListView.as_view(),
         name='data_list_success'),
    path(
        'data/<int:pk>/success/',
        data_success_detail,
        name='data_success_detail',
    ),

    # path('data-list/', QuarryMinerDataListView.as_view(), name='data_list'),
    # path(
    #     'miner-data/<int:pk>/',
    #     miner_data_detail,
    #     name='miner_data',
    # ),
    # path(
    #     'miner-data/<int:pk>/production-statistic/',
    #     production_statistic_detail,
    #     name='production_statistic',
    # ),
    # path(
    #     'miner-data/<int:pk>/sales-submission/',
    #     sales_submission_detail,
    #     name='sales_submission',
    # ),
    # path(
    #     'miner-data/<int:pk>/final-uses/',
    #     final_uses_detail,
    #     name='final_uses',
    # ),
    # path(
    #     'miner-data/<int:pk>/local-worker/',
    #     local_worker_detail,
    #     name='local_worker',
    # ),
    # path(
    #     'miner-data/<int:pk>/foreign-worker/',
    #     foreign_worker_detail,
    #     name='foreign_worker',
    # ),
    # path(
    #     'miner-data/<int:pk>/machinery/',
    #     machinery_detail,
    #     name='machinery',
    # ),
    # path(
    #     'miner-data/<int:pk>/daily-explosive/',
    #     daily_explosive_detail,
    #     name='daily_explosive',
    # ),
    # path(
    #     'miner-data/<int:pk>/energy-supply/',
    #     energy_supply_detail,
    #     name='energy_supply',
    # ),
    # path(
    #     'miner-data/<int:pk>/operating-record/',
    #     operating_record_detail,
    #     name='operating_record',
    # ),
    # path(
    #     'miner-data/<int:pk>/royalties/',
    #     royalties_detail,
    #     name='royalties',
    # ),
    # path(
    #     'miner-data/<int:pk>/other/',
    #     other_detail,
    #     name='other',
    # ),
]
