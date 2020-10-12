from django.urls import path

from .views import LoginView, LogoutView, RegistrationView, UserListView, UserListViews, ProfileView, PasswordChangeView, UserUpdate

app_name = 'account'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('<int:pk>/update/', UserUpdate.as_view(), name='updateuser'),
    path('usersList/', UserListViews.as_view(), name='user_listView'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password/', PasswordChangeView.as_view(), name='password-change'),
]
