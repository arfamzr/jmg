from ..views.state_admin import quarry_report_input, quarry_report
from django.urls import path

app_name = 'state_admin'


urlpatterns = [
    path('quarry/input/', quarry_report_input, name='quarry_input'),
    path('quarry/', quarry_report, name='quarry'),
]
