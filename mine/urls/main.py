from django.urls import path, include

from ..views.main import (
    # data
    DataListView,
    DataCreateView,
    data_delete,
    data_detail,

    # statistic
    statistic_edit,
    MainStatisticCreateView,
    MainStatisticUpdateView,
    main_statistic_delete,
    main_statistic_detail,
    SideStatisticCreateView,
    SideStatisticUpdateView,
    side_statistic_delete,
    side_statistic_detail,

    # local worker
    local_worker_edit,

    # foreign worker
    foreign_worker_edit,

    # machinery
    machinery_edit,

    # energy supply
    energy_supply_edit,

    # operating record
    operating_record_edit,

    # MineMinerListView,
    # add_report,
    # miner_data_delete,
    # miner_data_detail,
    # statistic_detail,
    # local_worker_detail,
    # foreign_worker_detail,
    # machinery_detail,
    # energy_supply_detail,
    # operating_record_detail,
    # get_comment_data,
)

app_name = 'mine'

urlpatterns = [
    # data
    path('data/', DataListView.as_view(), name='data_list'),
    path('data/create/', DataCreateView.as_view(), name='data_create'),
    path(
        'data/<int:pk>/delete/',
        data_delete,
        name='data_delete',
    ),
    path(
        'data/<int:pk>/',
        data_detail,
        name='data_detail',
    ),

    # statistic
    path(
        '<int:pk>/statistic/',
        statistic_edit,
        name='statistic_edit'
    ),
    path(
        '<int:pk>/main-statistic/create/',
        MainStatisticCreateView.as_view(),
        name='main_statistic_create'
    ),
    path(
        'main-statistic/<int:pk>/update/',
        MainStatisticUpdateView.as_view(),
        name='main_statistic_update'
    ),
    path(
        'main-statistic/<int:pk>/delete/',
        main_statistic_delete,
        name='main_statistic_delete'
    ),
    path(
        'data/main-statistic/<int:pk>/',
        main_statistic_detail,
        name='main_statistic_detail'
    ),
    path(
        '<int:pk>/side-statistic/create/',
        SideStatisticCreateView.as_view(),
        name='side_statistic_create'
    ),
    path(
        'side-statistic/<int:pk>/update/',
        SideStatisticUpdateView.as_view(),
        name='side_statistic_update'
    ),
    path(
        'side-statistic/<int:pk>/delete/',
        side_statistic_delete,
        name='side_statistic_delete'
    ),
    path(
        'data/side-statistic/<int:pk>/',
        side_statistic_detail,
        name='side_statistic_detail'
    ),

    # local worker
    path(
        '<int:pk>/local-worker/',
        local_worker_edit,
        name='local_worker_edit'
    ),

    # foreign worker
    path(
        '<int:pk>/foreign-worker/',
        foreign_worker_edit,
        name='foreign_worker_edit'
    ),

    # machinery
    path(
        '<int:pk>/machinery/',
        machinery_edit,
        name='machinery_edit'
    ),

    # energy supply
    path(
        '<int:pk>/energy-supply/',
        energy_supply_edit,
        name='energy_supply_edit'
    ),

    # operating record
    path(
        '<int:pk>/operating-record/',
        operating_record_edit,
        name='operating_record_edit'
    ),

    # user include
    path('state/', include('mine.urls.state', namespace='state')),
    path('state-admin/', include('mine.urls.state_admin', namespace='state_admin')),
    path('hq/', include('mine.urls.hq', namespace='hq')),

    # path('', MineMinerListView.as_view(), name='list'),
    # path('<int:pk>/add-report/', add_report, name='add_report'),
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
    # path(
    #     'miner-data/<int:pk>/get-comment/',
    #     get_comment_data,
    #     name='get_comment'
    # )
]
