from django.contrib.auth.views import PasswordChangeView as DjangoPasswordChangeView
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, resolve_url
from django.views.generic import FormView, ListView, TemplateView
from django.contrib.auth.views import (
    LoginView as DjangoLoginView,
    LogoutView as DjangoLogoutView,
)

from .models import User
from .forms import AuthenticationForm, UserCreationForm


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


class RegistrationView(FormView):
    form_class = UserCreationForm
    template_name = 'account/registration.html'
    redirect_authenticated_user = True

    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data['username']
        raw_password = form.cleaned_data['password1']
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'JMG Registration'
        return context

    def get_success_url(self):
        return resolve_url(settings.LOGIN_REDIRECT_URL)


class UserListView(ListView):
    template_name = 'account/user_list.html'
    model = User
    paginate_by = 8
    ordering = ['id']

    def get_queryset(self):
        try:
            name = self.request.GET['q']
        except:
            name = ''
        if (name != ''):
            object_list = self.model.objects.filter(username__icontains=name)
        else:
            object_list = self.model.objects.all()
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Pengguna'
        return context

class ProfileView(TemplateView):
    template_name = 'account/profile/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(self.request.user.is_industry)
        context["title"] = 'Profile'
        return context

class PasswordChangeView(DjangoPasswordChangeView):
    template_name = 'account/password/form.html'
    success_url = '/dashboard/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(self.request.user.is_industry)
        context["title"] = 'Update Password'
        return context
