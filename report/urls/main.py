from django.urls import path, include

app_name = 'report'

urlpatterns = [
    path('state-admin/', include('report.urls.state_admin', namespace='state_admin')),
]
