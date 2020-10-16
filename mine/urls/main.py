from django.urls import path, include

from ..views.main import (
    MineMinerListView,
    add_report,
    MineMinerDataListView,
    statistic_edit,
    local_worker_edit,
    foreign_worker_edit,
    machinery_edit,
    energy_supply_edit,
    operating_record_edit,
    miner_data_delete,
    miner_data_detail,
    statistic_detail,
    local_worker_detail,
    foreign_worker_detail,
    machinery_detail,
    energy_supply_detail,
    operating_record_detail,
    get_comment_data,
)

app_name = 'mine'

urlpatterns = [
    path('', MineMinerListView.as_view(), name='list'),
    path('<int:pk>/add-report/', add_report, name='add_report'),
    path('data-list/', MineMinerDataListView.as_view(), name='data_list'),
    path('state/', include('mine.urls.state', namespace='state')),
    path('state-admin/', include('mine.urls.state_admin', namespace='state_admin')),
    path(
        '<int:pk>/statistic/',
        statistic_edit,
        name='statistic_edit'
    ),
    path(
        '<int:pk>/local-worker/',
        local_worker_edit,
        name='local_worker_edit'
    ),
    path(
        '<int:pk>/foreign-worker/',
        foreign_worker_edit,
        name='foreign_worker_edit'
    ),
    path(
        '<int:pk>/machinery/',
        machinery_edit,
        name='machinery_edit'
    ),
    path(
        '<int:pk>/energy-supply/',
        energy_supply_edit,
        name='energy_supply_edit'
    ),
    path(
        '<int:pk>/operating-record/',
        operating_record_edit,
        name='operating_record_edit'
    ),
    path(
        'miner-data/<int:pk>/delete/edit/',
        miner_data_delete,
        name='miner_data_delete',
    ),
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
    path(
        'miner-data/<int:pk>/get-comment/',
        get_comment_data,
        name='get_comment'
    )
]
