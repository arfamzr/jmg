from django.urls import path, include

from ..views.state_admin import (
    CompanyListView,
    CompanyCreateView,
    company_detail,
    CompanyUpdateView,
    add_employee,
    toggle_active,
    company_add_employee,
    company_remove_employee,
)

app_name = 'state_admin'

urlpatterns = [
    path('', CompanyListView.as_view(), name='list'),
    path('create/', CompanyCreateView.as_view(), name='create'),
    path('<int:pk>/', company_detail, name='detail'),
    path('<int:pk>/update/', CompanyUpdateView.as_view(), name='update'),
    path('<int:pk>/toggle-active/', toggle_active, name='toggle_active'),
    path('<int:pk>/add-employee/', add_employee, name='add_employee'),
    path(
        '<int:company_pk>/add-employee/<int:user_pk>/',
        company_add_employee,
        name='company_add_employee',
    ),
    path(
        'remove-employee/<int:pk>/',
        company_remove_employee,
        name='company_remove_employee',
    ),
]
