from django.urls import path

from ..views.hq import quarry_graph

app_name = 'hq'


urlpatterns = [
    path('quarry/graph/input/', quarry_graph, name='quarry_graph'),
]
