from django.urls import path

from ..views.state_admin import quarry_report_input, quarry_report, mine_report_input, mine_report

app_name = 'state_admin'

urlpatterns = [
    path('quarry/input/', quarry_report_input, name='quarry_input'),
    path('quarry/', quarry_report, name='quarry'),
    path('mine/input/', mine_report_input, name='mine_input'),
    path('mine/', mine_report, name='mine'),
]
