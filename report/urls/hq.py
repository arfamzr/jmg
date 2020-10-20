from django.urls import path

from ..views.hq import quarry_report_input, quarry_report, quarry_graph

app_name = 'hq'

urlpatterns = [
    path('quarry/input/', quarry_report_input, name='quarry_input'),
    path('quarry/', quarry_report, name='quarry'),
    path('quarry/graph/input/', quarry_graph, name='quarry_graph'),
]
