from account.views.main import profile
from django.contrib.auth.models import Group
from django.shortcuts import render, get_object_or_404, Http404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, DetailView, UpdateView

from company.models import Company, Employee
from quarry.models import Quarry, QuarryMiner

from ..models import User, Profile
from ..forms.state_admin import UserCreationForm, UserForm, ProfileForm, PasswordResetForm


class UserListView(ListView):
    template_name = 'account/state_admin/user/list.html'
    model = User
    paginate_by = 8
    ordering = ['-id']

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            profile__state=self.request.user.profile.state,
            groups__name__in=['Industry'])
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
        context["title"] = 'Senarai Pengguna Sistem'
        return context


class StateListView(ListView):
    template_name = 'account/state_admin/user/state_list.html'
    model = User
    paginate_by = 8
    ordering = ['-id']

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            profile__state=self.request.user.profile.state,
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
        context["title"] = 'Senarai JMG state'
        return context


class UserRegistrationView(FormView):
    form_class = UserCreationForm
    template_name = 'account/state_admin/user/registration.html'
    success_url = reverse_lazy('account:state_admin:user_list')

    def form_valid(self, form):
        user = form.save()
        group = Group.objects.get(name='Industry')
        group.user_set.add(user)
        profile = Profile(user=user, state=self.request.user.profile.state)
        profile.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Daftar Pengguna'
        return context


class StateRegistrationView(FormView):
    form_class = UserCreationForm
    template_name = 'account/state_admin/user/registration.html'
    success_url = reverse_lazy('account:state_admin:state_list')

    def form_valid(self, form):
        user = form.save()
        group = Group.objects.get(name='JMG State')
        group.user_set.add(user)
        profile = Profile(user=user, state=self.request.user.profile.state)
        # profile = Profile(user=user, state=form.cleaned_data.get('state'))
        profile.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Daftar JMG State'
        return context


def user_detail(request, pk):
    each_user = get_object_or_404(User, pk=pk)

    context = {
        'each_user': each_user,
        'title': 'Maklumat Pengguna',
    }

    return render(request, 'account/state_admin/user/detail.html', context)


class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'account/state_admin/user/update.html'
    context_object_name = 'each_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Update Pengguna'
        return context


def state_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('account:state_admin:state_list')
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=user.profile)

    context = {
        'title': 'Update State',
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'account/state_admin/state/update.html', context)


def user_update_password(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            raw_password = form.cleaned_data.get('password1')
            user.set_password(raw_password)
            user.save()
            return redirect('dashboard:dashboard')
    else:
        form = PasswordResetForm()

    context = {
        'title': f'Reset Password for {user.username}',
        'user': user,
        'form': form,
    }
    return render(request, 'account/state_admin/user/reset_password.html', context)


def user_toggle_active(request, pk):
    each_user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        if each_user.is_active == True:
            each_user.is_active = False
        else:
            each_user.is_active = True
        each_user.save()
        return redirect('account:state_admin:user_list')

    context = {
        'each_user': each_user,
    }

    return render(request, 'account/state_admin/user/toggle_active.html', context)
