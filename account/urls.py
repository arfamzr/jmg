from django.urls import path

from .views import LoginView, LogoutView, RegistrationView, UserListView

app_name = 'account'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('users/', UserListView.as_view(), name='user_list'),
]
