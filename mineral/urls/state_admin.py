from django.urls import path

from ..views.state_admin import (
    # process factory
    ProcessFactoryListView,
    ProcessFactoryCreateView,
    ProcessFactoryUpdateView,
    process_factory_toggle_active,

    # process manager
    ManagerListView,
    manager_create,
    manager_update,
    manager_choose_operator,
    manager_add_operator,
    manager_toggle_active,
    get_manager_data,

    # data
    DataListView,
    DataSuccessListView,
    data_detail,
    data_success_detail,
)

app_name = 'state_admin'

urlpatterns = [
    # process factory
    path('process-factory/', ProcessFactoryListView.as_view(),
         name='process_factory_list'),
    path('process-factory/create/', ProcessFactoryCreateView.as_view(),
         name='process_factory_create'),
    path('process-factory/<int:pk>/update/',
         ProcessFactoryUpdateView.as_view(), name='process_factory_update'),
    path('process-factory/<int:pk>/toggle-active/',
         process_factory_toggle_active, name='process_factory_toggle_active'),

    # process manager
    path('manager/', ManagerListView.as_view(), name='manager_list'),
    path('<int:pk>/manager/create/', manager_create,
         name='manager_create'),
    path('manager/<int:pk>/update/',
         manager_update, name='manager_update'),
    #     path('manager/<int:pk>/choose-operator/',
    #          manager_choose_operator, name='manager_choose_operator'),
    #     path('manager/<int:manager_pk>/add-operator/<int:operator_pk>/',
    #          manager_add_operator, name='manager_add_operator'),
    path('manager/<int:pk>/toggle-active/',
         manager_toggle_active, name='manager_toggle_active'),
    path(
        'manager/<int:pk>/get-manager-data/',
        get_manager_data,
        name='get_manager_data'
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
]
