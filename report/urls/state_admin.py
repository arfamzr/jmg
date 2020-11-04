from django.urls import path

# from ..views.state_admin import quarry_report_input, quarry_report, quarry_graph, mine_report_input, mine_report, mine_graph

from ..views.state_admin import (
    mine_report,
)

app_name = 'state_admin'

urlpatterns = [
    path('mine/', mine_report, name='mine_report'),
    # path('quarry/input/', quarry_report_input, name='quarry_input'),
    # path('quarry/', quarry_report, name='quarry'),
    # path('quarry/graph/input/', quarry_graph, name='quarry_graph'),
    # path('mine/', mine_report, name='mine'),
    # path('mine/graph/input/', mine_graph, name='mine_graph'),
]
