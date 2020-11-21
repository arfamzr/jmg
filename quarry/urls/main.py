from django.urls import path, include

from ..views.main import (
    # data
    DataListView,
    DataCreateView,
    data_delete,
    data_detail,

    # production statistic
    production_statistic_edit,
    MainProductionStatisticCreateView,
    MainProductionStatisticUpdateView,
    main_production_statistic_delete,
    main_production_statistic_detail,
    SideProductionStatisticCreateView,
    SideProductionStatisticUpdateView,
    side_production_statistic_delete,
    side_production_statistic_detail,

    # sales submission
    sales_submission_edit,
    SalesSubmissionCreateView,
    SalesSubmissionUpdateView,
    sales_submission_delete,
    sales_submission_detail,

    # final uses
    final_uses_edit,

    # local worker
    local_worker_edit,

    # foreign worker
    foreign_worker_edit,

    # machiner
    machinery_edit,

    # daily explosive
    daily_explosive_edit,
    DailyExplosiveCreateView,
    DailyExplosiveUpdateView,
    daily_explosive_delete,

    # energy supply
    energy_supply_edit,

    # operating record
    operating_record_edit,

    # royalties
    royalties_edit,

    # other
    other_edit,

    # summary
    data_summary,

    # QuarryMinerListView,
    # add_report,
    # QuarryMinerDataListView,
    # production_statistic_edit,
    # sales_submission_edit,
    # miner_data_delete,
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
    # get_comment_data,
)


app_name = 'quarry'

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

    # production statistic
    path(
        '<int:pk>/production-statistic/',
        production_statistic_edit,
        name='production_statistic_edit'
    ),
    path(
        '<int:pk>/main-production-statistic/create/',
        MainProductionStatisticCreateView.as_view(),
        name='main_production_statistic_create'
    ),
    path(
        'main-production-statistic/<int:pk>/update/',
        MainProductionStatisticUpdateView.as_view(),
        name='main_production_statistic_update'
    ),
    path(
        'main-production-statistic/<int:pk>/delete/',
        main_production_statistic_delete,
        name='main_production_statistic_delete'
    ),
    path(
        'data/main-production-statistic/<int:pk>/',
        main_production_statistic_detail,
        name='main_production_statistic_detail'
    ),
    path(
        '<int:pk>/side-production-statistic/create/',
        SideProductionStatisticCreateView.as_view(),
        name='side_production_statistic_create'
    ),
    path(
        'side-production-statistic/<int:pk>/update/',
        SideProductionStatisticUpdateView.as_view(),
        name='side_production_statistic_update'
    ),
    path(
        'side-production-statistic/<int:pk>/delete/',
        side_production_statistic_delete,
        name='side_production_statistic_delete'
    ),
    path(
        'data/side-production-statistic/<int:pk>/',
        side_production_statistic_detail,
        name='side_production_statistic_detail'
    ),

    # sales submission
    path(
        'data/<int:pk>/sales-submission/',
        sales_submission_edit,
        name='sales_submission_edit'
    ),
    path(
        'data/<int:pk>/sales-submission/create/',
        SalesSubmissionCreateView.as_view(),
        name='sales_submission_create'
    ),
    path(
        'data/sales-submission/<int:pk>/update/',
        SalesSubmissionUpdateView.as_view(),
        name='sales_submission_update'
    ),
    path(
        'data/sales-submission/<int:pk>/delete/',
        sales_submission_delete,
        name='sales_submission_delete'
    ),
    path(
        'data/sales-submission/<int:pk>/',
        sales_submission_detail,
        name='sales_submission_detail'
    ),

    # final uses
    path(
        'data/<int:pk>/final-uses/edit/',
        final_uses_edit,
        name='final_uses_edit',
    ),

    # local worker
    path(
        'data/<int:pk>/local-worker/edit/',
        local_worker_edit,
        name='local_worker_edit',
    ),

    # foreign worker
    path(
        'data/<int:pk>/foreign-worker/edit/',
        foreign_worker_edit,
        name='foreign_worker_edit',
    ),

    # machinery
    path(
        'data/<int:pk>/machinery/edit/',
        machinery_edit,
        name='machinery_edit',
    ),

    # daily explosive
    path(
        'data/<int:pk>/daily-explosive/edit/',
        daily_explosive_edit,
        name='daily_explosive_edit',
    ),
    path(
        'data/<int:pk>/daily-explosive/create/',
        DailyExplosiveCreateView.as_view(),
        name='daily_explosive_create'
    ),
    path(
        'data/daily-explosive/<int:pk>/update/',
        DailyExplosiveUpdateView.as_view(),
        name='daily_explosive_update'
    ),
    path(
        'data/daily-explosive/<int:pk>/delete/',
        daily_explosive_delete,
        name='daily_explosive_delete'
    ),

    # energy supply
    path(
        'data/<int:pk>/energy-supply/edit/',
        energy_supply_edit,
        name='energy_supply_edit',
    ),

    # operating record
    path(
        'data/<int:pk>/operating-record/edit/',
        operating_record_edit,
        name='operating_record_edit',
    ),

    # royalties
    path(
        'data/<int:pk>/royalties/edit/',
        royalties_edit,
        name='royalties_edit',
    ),

    # other
    path(
        'data/<int:pk>/other/edit/',
        other_edit,
        name='other_edit',
    ),

    # summary
    path(
        'data/<int:pk>/summary/',
        data_summary,
        name='data_summary',
    ),

    # user include
    path('state/', include('quarry.urls.state', namespace='state')),
    path('state-admin/', include('quarry.urls.state_admin', namespace='state_admin')),
    path('hq/', include('quarry.urls.hq', namespace='hq')),

    # path('', QuarryMinerListView.as_view(), name='list'),
    # path('<int:pk>/add-report/', add_report, name='add_report'),
    # path('data-list/', QuarryMinerDataListView.as_view(), name='data_list'),
    # path(
    #     'data/<int:pk>/production-statistic/edit/',
    #     production_statistic_edit,
    #     name='production_statistic_edit',
    # ),
    # path(
    #     'data/<int:pk>/sales-submission/edit/',
    #     sales_submission_edit,
    #     name='sales_submission_edit',
    # ),
    # path(
    #     'data/<int:pk>/delete/edit/',
    #     miner_data_delete,
    #     name='miner_data_delete',
    # ),
    # path(
    #     'data/<int:pk>/',
    #     miner_data_detail,
    #     name='miner_data',
    # ),
    # path(
    #     'data/<int:pk>/production-statistic/',
    #     production_statistic_detail,
    #     name='production_statistic',
    # ),
    # path(
    #     'data/<int:pk>/sales-submission/',
    #     sales_submission_detail,
    #     name='sales_submission',
    # ),
    # path(
    #     'data/<int:pk>/final-uses/',
    #     final_uses_detail,
    #     name='final_uses',
    # ),
    # path(
    #     'data/<int:pk>/local-worker/',
    #     local_worker_detail,
    #     name='local_worker',
    # ),
    # path(
    #     'data/<int:pk>/foreign-worker/',
    #     foreign_worker_detail,
    #     name='foreign_worker',
    # ),
    # path(
    #     'data/<int:pk>/machinery/',
    #     machinery_detail,
    #     name='machinery',
    # ),
    # path(
    #     'data/<int:pk>/daily-explosive/',
    #     daily_explosive_detail,
    #     name='daily_explosive',
    # ),
    # path(
    #     'data/<int:pk>/energy-supply/',
    #     energy_supply_detail,
    #     name='energy_supply',
    # ),
    # path(
    #     'data/<int:pk>/operating-record/',
    #     operating_record_detail,
    #     name='operating_record',
    # ),
    # path(
    #     'data/<int:pk>/royalties/',
    #     royalties_detail,
    #     name='royalties',
    # ),
    # path(
    #     'data/<int:pk>/other/',
    #     other_detail,
    #     name='other',
    # ),
    # path(
    #     'data/<int:pk>/get-comment/',
    #     get_comment_data,
    #     name='get_comment'
    # ),
]
