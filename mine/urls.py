from django.urls import path

from . import views

app_name = 'mine'

urlpatterns = [
    path('', views.MineListView.as_view(), name='list'),
    # path('list/', views.MineListsView.as_view(), name='listmine'),
    # path('list-state/', views.MineStateListView.as_view(), name='list_state'),
    # path('list-state-admin/', views.MineStateAdminListView.as_view(),
    #      name='list_state_admin'),
    # path('list-hq/', views.MineHQListView.as_view(),
    #      name='list_hq'),
    # path('create/', views.MineCreateView.as_view(), name='create'),
    # path('update/<int:pk>/', views.MineUpdateView.as_view(), name='update'),
    # path(
    #     '<int:pk>/statistic/',
    #     views.statistic_edit,
    #     name='statistic_edit'
    # ),
    # path(
    #     '<int:pk>/local-worker/',
    #     views.local_worker_edit,
    #     name='local_worker_edit'
    # ),
    # path(
    #     '<int:pk>/foreign-worker/',
    #     views.foreign_worker_edit,
    #     name='foreign_worker_edit'
    # ),
    # path(
    #     '<int:pk>/machinery/',
    #     views.machinery_edit,
    #     name='machinery_edit'
    # ),
    # path(
    #     '<int:pk>/energy-supply/',
    #     views.energy_supply_edit,
    #     name='energy_supply_edit'
    # ),
    # path(
    #     '<int:pk>/operating-record/',
    #     views.operating_record_edit,
    #     name='operating_record_edit'
    # ),
    # path('readonly/<int:pk>/', views.mine_readonly, name='readonly'),
    # path(
    #     'readonly/<int:pk>/statistic/',
    #     views.statistic_readonly,
    #     name='statistic_readonly'
    # ),
    # path(
    #     'readonly/<int:pk>/local-worker/',
    #     views.local_worker_readonly,
    #     name='local_worker_readonly'
    # ),
    # path(
    #     'readonly/<int:pk>/foreign-worker/',
    #     views.foreign_worker_readonly,
    #     name='foreign_worker_readonly'
    # ),
    # path(
    #     'readonly/<int:pk>/machinery/',
    #     views.machinery_readonly,
    #     name='machinery_readonly'
    # ),
    # path(
    #     'readonly/<int:pk>/energy-supply/',
    #     views.energy_supply_readonly,
    #     name='energy_supply_readonly'
    # ),
    # path(
    #     'readonly/<int:pk>/operating-record/',
    #     views.operating_record_readonly,
    #     name='operating_record_readonly'
    # ),
    # path(
    #     '<int:pk>/submit/',
    #     views.submit_mine,
    #     name='submit',
    # ),
    # path(
    #     'state/<int:pk>/approve/',
    #     views.state_approve_mine,
    #     name='state_approve',
    # ),
    # path(
    #     'state/<int:pk>/reject/',
    #     views.state_reject_mine,
    #     name='state_reject',
    # ),
    # path(
    #     'state-admin/<int:pk>/approve/',
    #     views.state_admin_approve_mine,
    #     name='state_admin_approve',
    # ),
    # path(
    #     'state-admin/<int:pk>/reject/',
    #     views.state_admin_reject_mine,
    #     name='state_admin_reject',
    # ),
    # path(
    #     '<int:pk>/get-comment/',
    #     views.get_comment_mine,
    #     name='state_get_comment',
    # ),
]
