from django.urls import path

# from ..views.state_admin import quarry_report_input, quarry_report, quarry_graph, mine_report_input, mine_report, mine_graph

from ..views.state_admin import (
    # mine report
    mine_report,

    # quarry report
    quarry_report,

    # mine production graph
    mine_production_graph,

    # mine worker graph
    mine_worker_graph,

    # quarry production graph
    quarry_production_graph,

    # quarry worker graph
    quarry_worker_graph,

    # quarry royalties graph
    quarry_royalties_graph,
)

app_name = 'state_admin'

urlpatterns = [
    # mine report
    path('mine/', mine_report, name='mine_report'),

    # quarry report
    path('quarry/', quarry_report, name='quarry_report'),

    # mine production graph
    path('mine/graph/production/', mine_production_graph,
         name='mine_production_graph'),

    # mine worker graph
    path('mine/graph/worker/', mine_worker_graph,
         name='mine_worker_graph'),

    # quarry production graph
    path('quarry/graph/production/', quarry_production_graph,
         name='quarry_production_graph'),

    # quarry worker graph
    path('quarry/graph/worker/', quarry_worker_graph,
         name='quarry_worker_graph'),

    # quarry royalties graph
    path('quarry/graph/royalties/', quarry_royalties_graph,
         name='quarry_royalties_graph'),

    # path('quarry/input/', quarry_report_input, name='quarry_input'),
    # path('quarry/', quarry_report, name='quarry'),
    # path('quarry/graph/input/', quarry_graph, name='quarry_graph'),
    # path('mine/', mine_report, name='mine'),
    # path('mine/graph/input/', mine_graph, name='mine_graph'),
]
