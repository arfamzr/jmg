from django.urls import path, include

app_name = 'report'

urlpatterns = [
    path('state-admin/', include('report.urls.state_admin', namespace='state_admin')),
    path('hq/', include('report.urls.hq', namespace='hq')),
    path('executive/', include('report.urls.executive', namespace='executive')),
]
