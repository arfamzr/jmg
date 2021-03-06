from django.urls import path

from . import views

app_name = 'quarry'

urlpatterns = [
    path('', views.QuarryListView.as_view(), name='list'),
    # path('list/', views.QuarryListsView.as_view(), name='listquarry'),
    # path('list-state/', views.QuarryStateListView.as_view(), name='list_state'),
    # path('list-state-admin/', views.QuarryStateAdminListView.as_view(),
    #      name='list_state_admin'),
    # path('list-hq/', views.QuarryHQListView.as_view(),
    #      name='list_hq'),
    # path('create/', views.QuarryCreateView.as_view(), name='create'),
    # path('update/<int:pk>/', views.QuarryUpdateView.as_view(), name='update'),
    # path(
    #     '<int:pk>/production-statistic/',
    #     views.production_statistic_edit,
    #     name='production_statistic_edit',
    # ),
    # path(
    #     '<int:pk>/sales-submission/',
    #     views.sales_submission_edit,
    #     name='sales_submission_edit',
    # ),
    # path(
    #     '<int:pk>/final-uses/',
    #     views.final_uses_edit,
    #     name='final_uses_edit',
    # ),
    # path(
    #     '<int:pk>/local-worker/',
    #     views.local_worker_edit,
    #     name='local_worker_edit',
    # ),
    # path(
    #     '<int:pk>/foreign-worker/',
    #     views.foreign_worker_edit,
    #     name='foreign_worker_edit',
    # ),
    # path(
    #     '<int:pk>/machinery/',
    #     views.machinery_edit,
    #     name='machinery_edit',
    # ),
    # path(
    #     '<int:pk>/daily-explosive/',
    #     views.daily_explosive_edit,
    #     name='daily_explosive_edit',
    # ),
    # path(
    #     '<int:pk>/energy-supply/',
    #     views.energy_supply_edit,
    #     name='energy_supply_edit',
    # ),
    # path(
    #     '<int:pk>/operating-record/',
    #     views.operating_record_edit,
    #     name='operating_record_edit',
    # ),
    # path(
    #     '<int:pk>/royalties/',
    #     views.royalties_edit,
    #     name='royalties_edit',
    # ),
    # path(
    #     '<int:pk>/other/',
    #     views.other_edit,
    #     name='other_edit',
    # ),
    # path('readonly/<int:pk>/', views.quarry_readonly, name='readonly'),
    # path(
    #     'readonly/<int:pk>/production-statistic/',
    #     views.production_statistic_readonly,
    #     name='production_statistic_readonly',
    # ),
    # path(
    #     'readonly/<int:pk>/sales-submission/',
    #     views.sales_submission_readonly,
    #     name='sales_submission_readonly',
    # ),
    # path(
    #     'readonly/<int:pk>/final-uses/',
    #     views.final_uses_readonly,
    #     name='final_uses_readonly',
    # ),
    # path(
    #     'readonly/<int:pk>/local-worker/',
    #     views.local_worker_readonly,
    #     name='local_worker_readonly',
    # ),
    # path(
    #     'readonly/<int:pk>/foreign-worker/',
    #     views.foreign_worker_readonly,
    #     name='foreign_worker_readonly',
    # ),
    # path(
    #     'readonly/<int:pk>/machinery/',
    #     views.machinery_readonly,
    #     name='machinery_readonly',
    # ),
    # path(
    #     'readonly/<int:pk>/daily-explosive/',
    #     views.daily_explosive_readonly,
    #     name='daily_explosive_readonly',
    # ),
    # path(
    #     'readonly/<int:pk>/energy-supply/',
    #     views.energy_supply_readonly,
    #     name='energy_supply_readonly',
    # ),
    # path(
    #     'readonly/<int:pk>/operating-record/',
    #     views.operating_record_readonly,
    #     name='operating_record_readonly',
    # ),
    # path(
    #     'readonly/<int:pk>/royalties/',
    #     views.royalties_readonly,
    #     name='royalties_readonly',
    # ),
    # path(
    #     'readonly/<int:pk>/other/',
    #     views.other_readonly,
    #     name='other_readonly',
    # ),
    # path(
    #     '<int:pk>/submit/',
    #     views.submit_quarry,
    #     name='submit',
    # ),
    # path(
    #     'state/<int:pk>/approve/',
    #     views.state_approve_quarry,
    #     name='state_approve',
    # ),
    # path(
    #     'state/<int:pk>/reject/',
    #     views.state_reject_quarry,
    #     name='state_reject',
    # ),
    # path(
    #     'state-admin/<int:pk>/approve/',
    #     views.state_admin_approve_quarry,
    #     name='state_admin_approve',
    # ),
    # path(
    #     'state-admin/<int:pk>/reject/',
    #     views.state_admin_reject_quarry,
    #     name='state_admin_reject',
    # ),
    # path(
    #     '<int:pk>/get-comment/',
    #     views.get_comment_quarry,
    #     name='state_get_comment',
    # ),
]
