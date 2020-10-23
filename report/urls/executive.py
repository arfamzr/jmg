from django.urls import path

from ..views.executive import rocks_input, quarry_production_graph, quarry_royalties_graph

app_name = 'hq'

urlpatterns = [
    path('input/', rocks_input, name='input'),
    path('quarry/production/graph/', quarry_production_graph,
         name='quarry_production_graph'),
    path('quarry/royalties/graph/', quarry_royalties_graph,
         name='quarry_royalties_graph'),
]
