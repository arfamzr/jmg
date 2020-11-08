from django.urls import path

from ..views.state_admin import (
    # lease holder
    LeaseHolderListView,
    LeaseHolderCreateView,
    LeaseHolderUpdateView,
    lease_holder_toggle_active,

    # operator
    OperatorListView,
    OperatorCreateView,
    OperatorUpdateView,
    operator_toggle_active,

    # manager
    ManagerListView,
    manager_create,
    manager_update,
    manager_choose_operator,
    manager_add_operator,
    manager_toggle_active,
    get_manager_data,

    # quarry
    QuarryListView,
    QuarryCreateView,
    QuarryUpdateView,
    quarry_detail,
    toggle_active,

    # lot
    lot_list,
    LotCreateView,
    LotUpdateView,
    lot_delete,

    # rock
    rock_list,

    # main rock
    MainRockCreateView,
    MainRockUpdateView,
    main_rock_delete,

    # side rock
    SideRockCreateView,
    SideRockUpdateView,
    side_rock_delete,

    # data
    DataListView,
    DataSuccessListView,
    data_detail,
    data_success_detail,

    # QuarryListView,
    # QuarryCreateView,
    # QuarryUpdateView,
    # quarry_detail,
    # add_miner,
    # quarry_add_miner,
    # quarry_remove_miner,
    # toggle_active,
    # user_quarry_list,
    # QuarryMinerDataListView,
    # QuarryMinerDataSuccessListView,
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
    # quarry_graph,
)

app_name = 'state_admin'

urlpatterns = [
    # lease holder
    path('lease-holder/', LeaseHolderListView.as_view(), name='lease_holder_list'),
    path('lease-holder/create/', LeaseHolderCreateView.as_view(),
         name='lease_holder_create'),
    path('lease-holder/<int:pk>/update/',
         LeaseHolderUpdateView.as_view(), name='lease_holder_update'),
    path('lease-holder/<int:pk>/toggle-active/',
         lease_holder_toggle_active, name='lease_holder_toggle_active'),

    # manager
    path('manager/', ManagerListView.as_view(), name='manager_list'),
    path('<int:pk>/manager/create/', manager_create,
         name='manager_create'),
    path('manager/<int:pk>/update/',
         manager_update, name='manager_update'),
    path('manager/<int:pk>/choose-operator/',
         manager_choose_operator, name='manager_choose_operator'),
    path('manager/<int:manager_pk>/add-operator/<int:operator_pk>/',
         manager_add_operator, name='manager_add_operator'),
    path('manager/<int:pk>/toggle-active/',
         manager_toggle_active, name='manager_toggle_active'),
    path(
        'manager/<int:pk>/get-manager-data/',
        get_manager_data,
        name='get_manager_data'
    ),

    # operator
    path('operator/', OperatorListView.as_view(), name='operator_list'),
    path('operator/create/', OperatorCreateView.as_view(),
         name='operator_create'),
    path('operator/<int:pk>/update/',
         OperatorUpdateView.as_view(), name='operator_update'),
    path('operator/<int:pk>/toggle-active/',
         operator_toggle_active, name='operator_toggle_active'),

    # quarry
    path('', QuarryListView.as_view(), name='list'),
    path('<int:pk>/create/', QuarryCreateView.as_view(), name='create'),
    path('<int:pk>/update/', QuarryUpdateView.as_view(), name='update'),
    path('<int:pk>/detail/', quarry_detail, name='detail'),
    path('<int:pk>/toggle-active/', toggle_active, name='toggle_active'),

    # lot
    path(
        '<int:pk>/lot/',
        lot_list,
        name='lot_list'
    ),
    path(
        '<int:pk>/lot/create/',
        LotCreateView.as_view(),
        name='lot_create'
    ),
    path(
        'lot/<int:pk>/update/',
        LotUpdateView.as_view(),
        name='lot_update'
    ),
    path(
        'lot/<int:pk>/delete/',
        lot_delete,
        name='lot_delete'
    ),

    # rock
    path(
        '<int:pk>/rock/',
        rock_list,
        name='rock_list'
    ),

    # main rock
    path(
        '<int:pk>/main-rock/create/',
        MainRockCreateView.as_view(),
        name='main_rock_create'
    ),
    path(
        'main-rock/<int:pk>/update/',
        MainRockUpdateView.as_view(),
        name='main_rock_update'
    ),
    path(
        'main-rock/<int:pk>/delete/',
        main_rock_delete,
        name='main_rock_delete'
    ),

    # side rock
    path(
        '<int:pk>/side-rock/create/',
        SideRockCreateView.as_view(),
        name='side_rock_create'
    ),
    path(
        'side-rock/<int:pk>/update/',
        SideRockUpdateView.as_view(),
        name='side_rock_update'
    ),
    path(
        'side-rock/<int:pk>/delete/',
        side_rock_delete,
        name='side_rock_delete'
    ),

    # data
    path('data-list/', DataListView.as_view(), name='data_list'),
    path('data-list/success/', DataSuccessListView.as_view(),
         name='data_list_success'),
    path(
        'data/<int:pk>/',
        data_detail,
        name='data_detail',
    ),
    path(
        'data/<int:pk>/success/',
        data_success_detail,
        name='data_success_detail',
    ),

    # path('', QuarryListView.as_view(), name='list'),
    # path('create/', QuarryCreateView.as_view(), name='create'),
    # path('<int:pk>/update/', QuarryUpdateView.as_view(), name='update'),
    # path('<int:pk>/detail/', quarry_detail, name='detail'),
    # path('<int:pk>/graph/', quarry_graph, name='graph'),
    # path('<int:pk>/toggle-active/', toggle_active, name='toggle_active'),
    # path('<int:pk>/add-miner/', add_miner, name='add_miner'),
    # path('<int:quarry_pk>/add-miner/<int:user_pk>/',
    #      quarry_add_miner, name='quarry_add_miner'),
    # path('remove-miner/<int:pk>/',
    #      quarry_remove_miner, name='quarry_remove_miner'),
    # path('user-quarry/<int:pk>/',
    #      user_quarry_list, name='user_quarry_list'),
    # path('data-list/', QuarryMinerDataListView.as_view(), name='data_list'),
    # path('data-list/success/', QuarryMinerDataSuccessListView.as_view(), name='data_list_success'),
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
