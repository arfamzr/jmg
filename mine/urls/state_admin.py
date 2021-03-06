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

    # mine
    MineListView,
    MineCreateView,
    MineUpdateView,
    mine_detail,
    toggle_active,

    # data
    DataListView,
    DataSuccessListView,
    data_detail,
    data_success_detail,

    # add_miner,
    # mine_add_miner,
    # mine_remove_miner,
    # user_mine_list,
    statistic_detail,
    local_worker_detail,
    foreign_worker_detail,
    machinery_detail,
    energy_supply_detail,
    operating_record_detail,

    # mineral
    mineral_list,

    # main mineral
    MainMineralCreateView,
    MainMineralUpdateView,
    main_mineral_delete,

    # side mineral
    SideMineralCreateView,
    SideMineralUpdateView,
    side_mineral_delete,
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

    # mine
    path('', MineListView.as_view(), name='list'),
    path('<int:pk>/create/', MineCreateView.as_view(), name='create'),
    path('<int:pk>/update/', MineUpdateView.as_view(), name='update'),
    path('<int:pk>/detail/', mine_detail, name='detail'),
    path('<int:pk>/toggle-active/', toggle_active, name='toggle_active'),

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

    # path('<int:pk>/add-miner/', add_miner, name='add_miner'),
    # path('<int:mine_pk>/add-miner/<int:user_pk>/',
    #      mine_add_miner, name='mine_add_miner'),
    # path('remove-miner/<int:pk>/',
    #      mine_remove_miner, name='mine_remove_miner'),
    # path('user-mine/<int:pk>/',
    #      user_mine_list, name='user_mine_list'),
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

    # mineral
    path(
        '<int:pk>/mineral/',
        mineral_list,
        name='mineral_list'
    ),

    # main mineral
    path(
        '<int:pk>/main-mineral/create/',
        MainMineralCreateView.as_view(),
        name='main_mineral_create'
    ),
    path(
        'main-mineral/<int:pk>/update/',
        MainMineralUpdateView.as_view(),
        name='main_mineral_update'
    ),
    path(
        'main-mineral/<int:pk>/delete/',
        main_mineral_delete,
        name='main_mineral_delete'
    ),

    # side mineral
    path(
        '<int:pk>/side-mineral/create/',
        SideMineralCreateView.as_view(),
        name='side_mineral_create'
    ),
    path(
        'side-mineral/<int:pk>/update/',
        SideMineralUpdateView.as_view(),
        name='side_mineral_update'
    ),
    path(
        'side-mineral/<int:pk>/delete/',
        side_mineral_delete,
        name='side_mineral_delete'
    ),
]
