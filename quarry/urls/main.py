from django.urls import path, include

app_name = 'quarry'

urlpatterns = [
    path('state-admin/', include('quarry.urls.state_admin', namespace='state_admin'))
]
