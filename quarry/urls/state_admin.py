from django.urls import path

from ..views.state_admin import QuarryListView

app_name = 'state_admin'

urlpatterns = [
    path('', QuarryListView.as_view(), name='list')
]
