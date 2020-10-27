from django.urls import path

from ..views.state_admin import (
    QuarryListView,
    QuarryCreateView,
    QuarryUpdateView,
    quarry_detail,
    add_miner,
    quarry_add_miner,
    quarry_remove_miner,
    toggle_active,
    user_quarry_list,
    QuarryMinerDataListView,
    QuarryMinerDataSuccessListView,
    miner_data_detail,
    production_statistic_detail,
    sales_submission_detail,
    final_uses_detail,
    local_worker_detail,
    foreign_worker_detail,
    machinery_detail,
    daily_explosive_detail,
    energy_supply_detail,
    operating_record_detail,
    royalties_detail,
    other_detail,
)

app_name = 'state_admin'

urlpatterns = [
    path('', QuarryListView.as_view(), name='list'),
    path('create/', QuarryCreateView.as_view(), name='create'),
    path('<int:pk>/update/', QuarryUpdateView.as_view(), name='update'),
    path('<int:pk>/detail/', quarry_detail, name='detail'),
    path('<int:pk>/toggle-active/', toggle_active, name='toggle_active'),
    path('<int:pk>/add-miner/', add_miner, name='add_miner'),
    path('<int:quarry_pk>/add-miner/<int:user_pk>/',
         quarry_add_miner, name='quarry_add_miner'),
    path('remove-miner/<int:pk>/',
         quarry_remove_miner, name='quarry_remove_miner'),
    path('user-quarry/<int:pk>/',
         user_quarry_list, name='user_quarry_list'),
    path('data-list/', QuarryMinerDataListView.as_view(), name='data_list'),
    path('data-list/success/', QuarryMinerDataSuccessListView.as_view(), name='data_list_success'),
    path(
        'miner-data/<int:pk>/',
        miner_data_detail,
        name='miner_data',
    ),
    path(
        'miner-data/<int:pk>/production-statistic/',
        production_statistic_detail,
        name='production_statistic',
    ),
    path(
        'miner-data/<int:pk>/sales-submission/',
        sales_submission_detail,
        name='sales_submission',
    ),
    path(
        'miner-data/<int:pk>/final-uses/',
        final_uses_detail,
        name='final_uses',
    ),
    path(
        'miner-data/<int:pk>/local-worker/',
        local_worker_detail,
        name='local_worker',
    ),
    path(
        'miner-data/<int:pk>/foreign-worker/',
        foreign_worker_detail,
        name='foreign_worker',
    ),
    path(
        'miner-data/<int:pk>/machinery/',
        machinery_detail,
        name='machinery',
    ),
    path(
        'miner-data/<int:pk>/daily-explosive/',
        daily_explosive_detail,
        name='daily_explosive',
    ),
    path(
        'miner-data/<int:pk>/energy-supply/',
        energy_supply_detail,
        name='energy_supply',
    ),
    path(
        'miner-data/<int:pk>/operating-record/',
        operating_record_detail,
        name='operating_record',
    ),
    path(
        'miner-data/<int:pk>/royalties/',
        royalties_detail,
        name='royalties',
    ),
    path(
        'miner-data/<int:pk>/other/',
        other_detail,
        name='other',
    ),
]
