from django.urls import path

from .views import (
    QuarryListView,
    QuarryCreateView,
    QuarryUpdateView,
    production_statistic_edit,
    sales_submission_edit,
    final_uses_edit,
    local_worker_edit,
    foreign_worker_edit,
    machinery_edit,
    daily_explosive_edit,
    energy_supply_edit,
    operating_record_edit,
    royalties_edit,
    other_edit,
)

app_name = 'quarry'

urlpatterns = [
    path('', QuarryListView.as_view(), name='list'),
    path('create/', QuarryCreateView.as_view(), name='create'),
    path('update/<int:pk>/', QuarryUpdateView.as_view(), name='update'),
    path(
        '<int:pk>/production-statistic/',
        production_statistic_edit,
        name='production_statistic_edit'
    ),
    path(
        '<int:pk>/sales-submission/',
        sales_submission_edit,
        name='sales_submission_edit'
    ),
    path(
        '<int:pk>/final-uses/',
        final_uses_edit,
        name='final_uses_edit'
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
        '<int:pk>/daily-explosive/',
        daily_explosive_edit,
        name='daily_explosive_edit'
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
        '<int:pk>/royalties/',
        royalties_edit,
        name='royalties_edit'
    ),
    path(
        '<int:pk>/other/',
        other_edit,
        name='other_edit'
    ),
]
