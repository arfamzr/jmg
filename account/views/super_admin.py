from django.contrib.auth.models import Group
from django.shortcuts import render, get_object_or_404, Http404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, DetailView, UpdateView

from ..models import User, Profile
from ..forms.state_admin import UserCreationForm, UserForm, ProfileForm, PasswordResetForm, StateForm
from ..forms.super_admin import HqUserCreationForm


# hq list
class HQListView(ListView):
    # template_name = 'account/super_admin/admin_user/list.html'
    template_name = 'account/super_admin/hq/list.html'
    model = User
    paginate_by = 8
    ordering = ['-profile__state']

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


# hq create
class HQRegistrationView(FormView):
    form_class = UserCreationForm
    template_name = 'account/super_admin/hq/registration.html'
    success_url = reverse_lazy('account:super_admin:hq_list')

    def form_valid(self, form):
        user = form.save()
        group = Group.objects.get(name='JMG HQ')
        group.user_set.add(user)
        profile = Profile(user=user, state=self.request.user.profile.state)
        # profile = Profile(user=user, state=form.cleaned_data.get('state'))
        profile.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Daftar JMG HQ'
        return context


# hq update
class HQUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'account/super_admin/hq/update.html'
    success_url = reverse_lazy('account:super_admin:hq_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Update JMG HQ'
        return context


# hq toggle active
def hq_toggle_active(request, pk):
    each_user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        if each_user.is_active == True:
            each_user.is_active = False
        else:
            each_user.is_active = True
        each_user.save()
        return redirect('account:super_admin:hq_list')

    context = {
        'each_user': each_user,
    }

    return render(request, 'account/super_admin/hq/toggle_active.html', context)


# state admin list
class AdminListView(ListView):
    # template_name = 'account/super_admin/admin_user/list.html'
    template_name = 'account/super_admin/state_admin/list.html'
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


# state admin create
class AdminRegistrationView(FormView):
    form_class = UserCreationForm
    template_name = 'account/super_admin/state_admin/registration.html'
    success_url = reverse_lazy('account:super_admin:state_admin_list')

    def form_valid(self, form):
        user = form.save()
        group = Group.objects.get(name='JMG State Admin')
        group.user_set.add(user)
        profile = Profile(user=user, state=self.request.user.profile.state)
        # profile = Profile(user=user, state=form.cleaned_data.get('state'))
        profile.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Daftar JMG Admin Negeri'
        return context


# state admin update
class AdminUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'account/super_admin/state_admin/update.html'
    success_url = reverse_lazy('account:super_admin:state_admin_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Update Admin Negeri'
        return context


# state admin toggle active
def state_admin_toggle_active(request, pk):
    each_user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        if each_user.is_active == True:
            each_user.is_active = False
        else:
            each_user.is_active = True
        each_user.save()
        return redirect('account:super_admin:state_admin_list')

    context = {
        'each_user': each_user,
    }

    return render(request, 'account/super_admin/state_admin/toggle_active.html', context)


# state admin update state
class AdminStateUpdateView(UpdateView):
    model = Profile
    form_class = StateForm
    template_name = 'account/super_admin/state_admin/state_update.html'
    success_url = reverse_lazy('account:super_admin:state_admin_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Update JMG Admin Negeri'
        return context


###############################################################################


# class HqListView(ListView):
#     template_name = 'account/super_admin/hq_user/list.html'
#     model = User
#     paginate_by = 8
#     ordering = ['-id']

#     def get_queryset(self):
#         queryset = super().get_queryset().filter(
#             groups__name__in=['JMG HQ'])
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
#         context["title"] = 'Senarai JMG HQ'
#         return context


# class AdminListView(ListView):
#     template_name = 'account/super_admin/admin_user/list.html'
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


# # class StateListView(ListView):
# #     template_name = 'account/state_admin/user/list.html'
# #     model = User
# #     paginate_by = 8
# #     ordering = ['-id']

# #     def get_queryset(self):
# #         queryset = super().get_queryset().filter(
# #             profile__state=self.request.user.profile.state,
# #             groups__name__in=['JMG State'])
# #         try:
# #             name = self.request.GET['q']
# #         except:
# #             name = ''
# #         if (name != ''):
# #             object_list = queryset.filter(username__icontains=name)
# #         else:
# #             object_list = queryset
# #         return object_list

# #     def get_context_data(self, **kwargs):
# #         context = super().get_context_data(**kwargs)
# #         context["title"] = 'Senarai JMG Negeri'
# #         return context


# class HqRegistrationView(FormView):
#     form_class = UserCreationForm
#     template_name = 'account/state_admin/user/registration.html'
#     success_url = reverse_lazy('account:super_admin:hq_list')

#     def form_valid(self, form):
#         user = form.save()
#         group = Group.objects.get(name='JMG HQ')
#         group.user_set.add(user)
#         # profile = Profile(user=user, state=self.request.user.profile.state)
#         profile = Profile(user=user, state=form.cleaned_data.get('state'))
#         profile.save()
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = 'Daftar JMG HQ'
#         return context


# class AdminRegistrationView(FormView):
#     form_class = HqUserCreationForm
#     template_name = 'account/state_admin/user/registration.html'
#     success_url = reverse_lazy('account:super_admin:admin_list')

#     def form_valid(self, form):
#         user = form.save()
#         group = Group.objects.get(name='JMG State Admin')
#         group.user_set.add(user)
#         # profile = Profile(user=user, state=self.request.user.profile.state)
#         profile = Profile(user=user, state=form.cleaned_data.get('state'))
#         profile.save()
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = 'Daftar JMG State Admin'
#         return context


# # class StateRegistrationView(FormView):
# #     form_class = UserCreationForm
# #     template_name = 'account/state_admin/user/registration.html'
# #     success_url = reverse_lazy('account:super_admin:hq_list')

# #     def form_valid(self, form):
# #         user = form.save()
# #         group = Group.objects.get(name='JMG State')
# #         group.user_set.add(user)
# #         profile = Profile(user=user, state=self.request.user.profile.state)
# #         # profile = Profile(user=user, state=form.cleaned_data.get('state'))
# #         profile.save()
# #         return super().form_valid(form)

# #     def get_context_data(self, **kwargs):
# #         context = super().get_context_data(**kwargs)
# #         context["title"] = 'Daftar JMG State'
# #         return context


# def hq_detail(request, pk):
#     each_user = get_object_or_404(User, pk=pk)

#     context = {
#         'each_user': each_user,
#         'title': 'Maklumat JMG HQ',
#     }

#     return render(request, 'account/super_admin/hq_user/detail.html', context)


# def admin_detail(request, pk):
#     each_user = get_object_or_404(User, pk=pk)

#     context = {
#         'each_user': each_user,
#         'title': 'Maklumat JMG Admin',
#     }

#     return render(request, 'account/super_admin/admin_user/detail.html', context)


# class HQUpdateView(UpdateView):
#     model = User
#     form_class = UserForm
#     template_name = 'account/super_admin/hq_user/update.html'
#     context_object_name = 'each_user'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = 'Update JMG HQ'
#         return context


# def admin_update(request, pk):
#     user = get_object_or_404(User, pk=pk)
#     if request.method == 'POST':
#         user_form = UserForm(request.POST, instance=user)
#         profile_form = ProfileForm(request.POST, instance=user.profile)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             return redirect('account:super_admin:admin_list')
#     else:
#         user_form = UserForm(instance=user)
#         profile_form = ProfileForm(instance=user.profile)

#     context = {
#         'title': 'Update JMG Admin State',
#         'user_form': user_form,
#         'profile_form': profile_form,
#     }

#     return render(request, 'account/super_admin/admin_user/update.html', context)


# def hq_toggle_active(request, pk):
#     each_user = get_object_or_404(User, pk=pk)
#     if request.method == 'POST':
#         if each_user.is_active == True:
#             each_user.is_active = False
#         else:
#             each_user.is_active = True
#         each_user.save()
#         return redirect('account:super_admin:hq_list')

#     context = {
#         'each_user': each_user,
#     }

#     return render(request, 'account/super_admin/hq_user/toggle_active.html', context)


# def admin_toggle_active(request, pk):
#     each_user = get_object_or_404(User, pk=pk)
#     if request.method == 'POST':
#         if each_user.is_active == True:
#             each_user.is_active = False
#         else:
#             each_user.is_active = True
#         each_user.save()
#         return redirect('account:super_admin:admin_list')

#     context = {
#         'each_user': each_user,
#     }

#     return render(request, 'account/super_admin/admin_user/toggle_active.html', context)


# def hq_update_password(request, pk):
#     user = get_object_or_404(User, pk=pk)
#     if request.method == 'POST':
#         form = PasswordResetForm(request.POST)
#         if form.is_valid():
#             raw_password = form.cleaned_data.get('password1')
#             user.set_password(raw_password)
#             user.save()
#             return redirect('dashboard:dashboard')
#     else:
#         form = PasswordResetForm()

#     context = {
#         'title': f'Reset Password for {user.username}',
#         'user': user,
#         'form': form,
#     }
#     return render(request, 'account/super_admin/hq_user/reset_password.html', context)


# def admin_update_password(request, pk):
#     user = get_object_or_404(User, pk=pk)
#     if request.method == 'POST':
#         form = PasswordResetForm(request.POST)
#         if form.is_valid():
#             raw_password = form.cleaned_data.get('password1')
#             user.set_password(raw_password)
#             user.save()
#             return redirect('dashboard:dashboard')
#     else:
#         form = PasswordResetForm()

#     context = {
#         'title': f'Reset Password for {user.username}',
#         'user': user,
#         'form': form,
#     }
#     return render(request, 'account/super_admin/admin_user/reset_password.html', context)
