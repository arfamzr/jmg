from django.urls import path, include

# from .views import CompanyListView, CompanyCreateView, CompanyUpdate, CompanyDetail

app_name = 'company'

urlpatterns = [
    # path('', CompanyListView.as_view(), name='list'),
    # path('create/', CompanyCreateView.as_view(), name='create'),
    # path('update/<int:pk>/', CompanyUpdate.as_view(), name='update'),
    # path('detail/<int:pk>/', CompanyDetail.as_view(), name='detail'),
    path('state/', include('company.urls.state', namespace='state')),
    path('state-admin/', include('company.urls.state_admin', namespace='state_admin')),
]
