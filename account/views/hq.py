from django.contrib.auth.models import Group
from django.shortcuts import render, get_object_or_404, Http404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, DetailView, UpdateView

from ..models import User, Profile
from ..forms.state_admin import UserCreationForm, UserForm, ProfileForm, PasswordResetForm


# state admin list
class AdminListView(ListView):
    # template_name = 'account/super_admin/admin_user/list.html'
    template_name = 'account/hq/state_admin/list.html'
    model = User
    paginate_by = 8
    ordering = ['-profile__state']

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            groups__name__in=['JMG State Admin'])
        try:
            name = self.request.GET['q']
        except:
            name = ''
        if (name != ''):
            object_list = queryset.filter(username__icontains=name)
        else:
            object_list = queryset
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Senarai JMG Admin Negeri'
        return context


# state list
class StateListView(ListView):
    # template_name = 'account/super_admin/admin_user/list.html'
    template_name = 'account/hq/state/list.html'
    model = User
    paginate_by = 8
    ordering = ['-profile__state']

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            groups__name__in=['JMG State'])
        try:
            name = self.request.GET['q']
        except:
            name = ''
        if (name != ''):
            object_list = queryset.filter(username__icontains=name)
        else:
            object_list = queryset
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Senarai JMG Negeri'
        return context


#######################################################################################


# class AdminListView(ListView):
#     # template_name = 'account/super_admin/admin_user/list.html'
#     template_name = 'account/hq/admin_user/list.html'
#     model = User
#     paginate_by = 8
#     ordering = ['-id']

#     def get_queryset(self):
#         queryset = super().get_queryset().filter(
#             groups__name__in=['JMG State Admin'])
#         try:
#             name = self.request.GET['q']
#         except:
#             name = ''
#         if (name != ''):
#             object_list = queryset.filter(username__icontains=name)
#         else:
#             object_list = queryset
#         return object_list

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = 'Senarai JMG Admin Negeri'
#         return context


# class StateListView(ListView):
#     # template_name = 'account/state_admin/user/state_list.html'
#     template_name = 'account/hq/user/state_list.html'
#     model = User
#     paginate_by = 8
#     ordering = ['-id']

#     def get_queryset(self):
#         queryset = super().get_queryset().filter(
#             profile__state=self.request.user.profile.state,
#             groups__name__in=['JMG State'])
#         try:
#             name = self.request.GET['q']
#         except:
#             name = ''
#         if (name != ''):
#             object_list = queryset.filter(username__icontains=name)
#         else:
#             object_list = queryset
#         return object_list

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = 'Senarai JMG state'
#         return context
