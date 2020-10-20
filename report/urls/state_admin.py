from django.urls import path

from ..views.state_admin import quarry_report_input, quarry_report, quarry_graph, mine_report_input, mine_report, mine_graph

app_name = 'state_admin'

urlpatterns = [
    path('quarry/input/', quarry_report_input, name='quarry_input'),
    path('quarry/', quarry_report, name='quarry'),
    path('quarry/graph/input/', quarry_graph, name='quarry_graph'),
    path('mine/input/', mine_report_input, name='mine_input'),
    path('mine/', mine_report, name='mine'),
    path('mine/graph/input/', mine_graph, name='mine_graph'),
]
