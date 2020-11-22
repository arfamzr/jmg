from django.contrib.auth.views import (
    LoginView as DjangoLoginView,
    LogoutView as DjangoLogoutView,
    PasswordChangeView as DjangoPasswordChangeView,
)
from django.shortcuts import render

from ..forms.main import AuthenticationForm
from ..forms.forms import PasswordChangeForm


class LoginView(DjangoLoginView):
    template_name = 'account/login.html'
    form_class = AuthenticationForm
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'JMG Log Masuk'
        return context


class LogoutView(DjangoLogoutView):
    pass


class PasswordChangeView(DjangoPasswordChangeView):
    template_name = 'account/password/form.html'
    form_class = PasswordChangeForm
    success_url = '/dashboard/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(self.request.user.is_industry)
        context["title"] = 'Kemaskini Kata Laluan'
        return context


def profile(request):
    context = {
        'title': 'Profile'
    }

    return render(request, 'account/profile/detail.html', context)
