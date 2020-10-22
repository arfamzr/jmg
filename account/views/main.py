from django.contrib.auth.views import (
    LoginView as DjangoLoginView,
    LogoutView as DjangoLogoutView,
    PasswordChangeView as DjangoPasswordChangeView,
)
from django.shortcuts import render

from ..forms.main import AuthenticationForm


class LoginView(DjangoLoginView):
    template_name = 'account/login.html'
    form_class = AuthenticationForm
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'JMG Login'
        return context


class LogoutView(DjangoLogoutView):
    pass


class PasswordChangeView(DjangoPasswordChangeView):
    template_name = 'account/password/form.html'
    success_url = '/dashboard/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(self.request.user.is_industry)
        context["title"] = 'Update Password'
        return context


def profile(request):
    context = {
        'title': 'Profile'
    }

    return render(request, 'account/profile/detail.html', context)
