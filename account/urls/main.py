from django.urls import path, include

from ..views.main import LoginView, LogoutView, PasswordChangeView

app_name = 'account'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-change/', PasswordChangeView.as_view(), name='password-change'),
    path("state/", include('account.urls.state', namespace='state')),
    path("state-admin/", include('account.urls.state_admin', namespace='state_admin')),
    path("super-admin/", include('account.urls.super_admin', namespace='super_admin')),
]
