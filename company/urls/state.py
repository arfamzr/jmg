from django.urls import path, include

from ..views.state import (
    CompanyListView,
    company_detail,
)

app_name = 'state'

urlpatterns = [
    path('', CompanyListView.as_view(), name='list'),
    path('<int:pk>/', company_detail, name='detail'),
]
