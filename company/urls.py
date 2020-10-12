from django.urls import path

from .views import CompanyListView, CompanyCreateView, CompanyUpdate

app_name = 'company'

urlpatterns = [
    path('', CompanyListView.as_view(), name='list'),
    path('create/', CompanyCreateView.as_view(), name='create'),
    path('update/<int:pk>/', CompanyUpdate.as_view(), name='update'),
]
