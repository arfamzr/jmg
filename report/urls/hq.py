from django.urls import path

# from ..views.hq import quarry_report_input, quarry_report, quarry_graph, mine_report_input, mine_report, mine_graph
from ..views.hq import (
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

    # mine production state graph
    mine_production_state_graph,

    # mine worker state graph
    mine_worker_state_graph,

    # quarry production state graph
    quarry_production_state_graph,

    # quarry worker state graph
    quarry_worker_state_graph,

    # quarry royalties state graph
    quarry_royalties_state_graph,

    # mine active graph
    mine_active_graph,

    # quarry active graph
    quarry_active_graph,
)

app_name = 'hq'

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

    # mine production state graph
    path('mine/graph/state-production/', mine_production_state_graph,
         name='mine_production_state_graph'),

    # mine worker state graph
    path('mine/graph/state-worker/', mine_worker_state_graph,
         name='mine_worker_state_graph'),

    # quarry production state graph
    path('quarry/graph/state-production/', quarry_production_state_graph,
         name='quarry_production_state_graph'),

    # quarry worker state graph
    path('quarry/graph/state-worker/', quarry_worker_state_graph,
         name='quarry_worker_state_graph'),

    # quarry royalties state graph
    path('quarry/graph/state-royalties/', quarry_royalties_state_graph,
         name='quarry_royalties_state_graph'),

    # mine active graph
    path('mine/graph/active/', mine_active_graph,
         name='mine_active_graph'),

    # quarry active graph
    path('quarry/graph/active/', quarry_active_graph,
         name='quarry_active_graph'),

    # path('quarry/input/', quarry_report_input, name='quarry_input'),
    # path('quarry/', quarry_report, name='quarry'),
    # path('quarry/graph/input/', quarry_graph, name='quarry_graph'),
    # path('mine/input/', mine_report_input, name='mine_input'),
    # path('mine/', mine_report, name='mine'),
    # path('mine/graph/input/', mine_graph, name='mine_graph'),
]
