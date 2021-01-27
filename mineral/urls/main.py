from django.urls import path, include

from ..views.main import (
    # data
    DataListView,
    DataCreateView,
    data_delete,
    data_detail,

    # process statistic
    process_statistic_edit,
    ProcessStatisticCreateView,
    ProcessStatisticUpdateView,
    process_statistic_delete,
    process_statistic_detail,

    # process submission
    process_submission_edit,
    ProcessSubmissionCreateView,
    ProcessSubmissionUpdateView,
    process_submission_delete,
    process_submission_detail,

    # local worker
    local_worker_edit,

    # foreign worker
    foreign_worker_edit,

    # machiner
    machinery_edit,

    # energy supply
    energy_supply_edit,

    # operating record
    operating_record_edit,

    # other
    other_edit,

    # summary
    data_summary,
)

app_name = 'mineral'

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

    # process statistic
    path(
        'data/<int:pk>/process-statistic/',
        process_statistic_edit,
        name='process_statistic_edit'
    ),
    path(
        'data/<int:pk>/process-statistic/create/',
        ProcessStatisticCreateView.as_view(),
        name='process_statistic_create'
    ),
    path(
        'data/process-statistic/<int:pk>/update/',
        ProcessStatisticUpdateView.as_view(),
        name='process_statistic_update'
    ),
    path(
        'data/process-statistic/<int:pk>/delete/',
        process_statistic_delete,
        name='process_statistic_delete'
    ),
    path(
        'data/process-statistic/<int:pk>/',
        process_statistic_detail,
        name='process_statistic_detail'
    ),

    # process submission
    path(
        'data/<int:pk>/process-submission/',
        process_submission_edit,
        name='process_submission_edit'
    ),
    path(
        'data/<int:pk>/process-submission/create/',
        ProcessSubmissionCreateView.as_view(),
        name='process_submission_create'
    ),
    path(
        'data/process-submission/<int:pk>/update/',
        ProcessSubmissionUpdateView.as_view(),
        name='process_submission_update'
    ),
    path(
        'data/process-submission/<int:pk>/delete/',
        process_submission_delete,
        name='process_submission_delete'
    ),
    path(
        'data/process-submission/<int:pk>/',
        process_submission_detail,
        name='process_submission_detail'
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
    path('state/', include('mineral.urls.state', namespace='state')),
    path('state-admin/', include('mineral.urls.state_admin', namespace='state_admin')),
    # path('hq/', include('mineral.urls.hq', namespace='hq')),
]
