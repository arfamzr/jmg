from django.contrib.auth.models import Group
from django.shortcuts import render, get_object_or_404, Http404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView

from ..models import User, Profile
from ..forms.state_admin import UserCreationForm
from ..forms.super_admin import HqUserCreationForm


class HqListView(ListView):
    template_name = 'account/super_admin/hq_user/list.html'
    model = User
    paginate_by = 8
    ordering = ['-id']

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            groups__name__in=['JMG HQ'])
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
        context["title"] = 'Senarai JMG HQ'
        return context


class AdminListView(ListView):
    template_name = 'account/super_admin/admin_user/list.html'
    model = User
    paginate_by = 8
    ordering = ['-id']

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


# class StateListView(ListView):
#     template_name = 'account/state_admin/user/list.html'
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
#         context["title"] = 'Senarai JMG Negeri'
#         return context


class HqRegistrationView(FormView):
    form_class = UserCreationForm
    template_name = 'account/state_admin/user/registration.html'
    success_url = reverse_lazy('account:super_admin:hq_list')

    def form_valid(self, form):
        user = form.save()
        group = Group.objects.get(name='JMG HQ')
        group.user_set.add(user)
        # profile = Profile(user=user, state=self.request.user.profile.state)
        profile = Profile(user=user, state=form.cleaned_data.get('state'))
        profile.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Daftar JMG HQ'
        return context


class AdminRegistrationView(FormView):
    form_class = HqUserCreationForm
    template_name = 'account/state_admin/user/registration.html'
    success_url = reverse_lazy('account:super_admin:admin_list')

    def form_valid(self, form):
        user = form.save()
        group = Group.objects.get(name='JMG State Admin')
        group.user_set.add(user)
        # profile = Profile(user=user, state=self.request.user.profile.state)
        profile = Profile(user=user, state=form.cleaned_data.get('state'))
        profile.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Daftar JMG State Admin'
        return context


# class StateRegistrationView(FormView):
#     form_class = UserCreationForm
#     template_name = 'account/state_admin/user/registration.html'
#     success_url = reverse_lazy('account:state_admin:state_list')

#     def form_valid(self, form):
#         user = form.save()
#         group = Group.objects.get(name='JMG State')
#         group.user_set.add(user)
#         profile = Profile(user=user, state=self.request.user.profile.state)
#         # profile = Profile(user=user, state=form.cleaned_data.get('state'))
#         profile.save()
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = 'Daftar JMG State'
#         return context


def hq_detail(request, pk):
    each_user = get_object_or_404(User, pk=pk)

    context = {
        'each_user': each_user,
        'title': 'Maklumat JMG HQ',
    }

    return render(request, 'account/super_admin/hq_user/detail.html', context)


def admin_detail(request, pk):
    each_user = get_object_or_404(User, pk=pk)

    context = {
        'each_user': each_user,
        'title': 'Maklumat JMG Admin',
    }

    return render(request, 'account/super_admin/admin_user/detail.html', context)
