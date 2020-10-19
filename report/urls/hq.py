from ..views.hq import quarry_report_input, quarry_report
from django.urls import path

app_name = 'hq'


urlpatterns = [
    path('quarry/input/', quarry_report_input, name='quarry_input'),
    path('quarry/', quarry_report, name='quarry'),
]
