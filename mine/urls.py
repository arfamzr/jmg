from django.urls import path

from .views import (
    MineListView,
    MineCreateView,
    MineUpdateView,
    statistic_edit,
    local_worker_edit,
    foreign_worker_edit,
    machinery_edit,
    energy_supply_edit,
    operating_record_edit,
)

app_name = 'mine'

urlpatterns = [
    path('', MineListView.as_view(), name='list'),
    path('create/', MineCreateView.as_view(), name='create'),
    path('update/<int:pk>/', MineUpdateView.as_view(), name='update'),
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
]
