from django.contrib.auth.models import Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponse, JsonResponse
from django.http import request
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView

from account.models import User, Profile
from account.forms.state_admin import UserCreationForm, UserForm, ProfileForm
from account.user_check import user_is_jmg_state_admin, UserIsJMGStateAdminMixin
from notification.notify import Notify

from ..models import (
    ProcessFactory,
    ProcessManager,
    ProcessData,
    ProcessStatistic,
    ProcessSubmission,
    LocalOperator,
    LocalContractor,
    ForeignOperator,
    ForeignContractor,
    InternalCombustionMachinery,
    ElectricMachinery,
    EnergySupply,
    OperatingRecord,
    Other,
    Approval,
)

from ..forms.state_admin import (
    ProcessFactoryForm,
    ProcessManagerForm,
)


# process factory views
class ProcessFactoryListView(UserIsJMGStateAdminMixin, ListView):
    template_name = 'mineral/state_admin/process_factory/list.html'
    model = ProcessFactory
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            state=self.request.user.profile.state)
        try:
            name = self.request.GET['q']
        except:
            name = ''
        if (name != ''):
            object_list = queryset.filter(name__icontains=name)
        else:
            object_list = queryset
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Senarai Kilang Mineral'
        return context


class ProcessFactoryCreateView(UserIsJMGStateAdminMixin, CreateView):
    template_name = 'mineral/state_admin/process_factory/form.html'
    model = ProcessFactory
    form_class = ProcessFactoryForm
    success_url = reverse_lazy('mineral:state_admin:process_factory_list')

    def form_valid(self, form):
        form.instance.state = self.request.user.profile.state
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Tambah Kilang Mineral'
        return context


class ProcessFactoryUpdateView(UserIsJMGStateAdminMixin, UpdateView):
    template_name = 'mineral/state_admin/process_factory/form.html'
    model = ProcessFactory
    form_class = ProcessFactoryForm
    success_url = reverse_lazy('mineral:state_admin:process_factory_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Kemaskini Kilang Mineral'
        return context


@user_is_jmg_state_admin()
def process_factory_toggle_active(request, pk):
    process_factory = get_object_or_404(ProcessFactory, pk=pk)
    if request.method == 'POST':
        if process_factory.status == True:
            process_factory.status = False
        else:
            process_factory.status = True
        process_factory.save()
        return redirect('mineral:state_admin:process_factory_list')

    context = {
        'process_factory': process_factory,
    }

    return render(request, 'mineral/state_admin/process_factory/toggle_active.html', context)


# process manager views
class ManagerListView(UserIsJMGStateAdminMixin, ListView):
    template_name = 'mineral/state_admin/manager/list.html'
    model = ProcessManager
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            user__profile__state=self.request.user.profile.state)
        try:
            name = self.request.GET['q']
        except:
            name = ''
        if (name != ''):
            object_list = queryset.filter(user_username__icontains=name)
        else:
            object_list = queryset
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Senarai Pengurus Kilang Proses'
        return context


@user_is_jmg_state_admin()
def manager_create(request, pk):
    process_factory = get_object_or_404(ProcessFactory, pk=pk)
    if request.method == 'POST':
        # manager_form = ProcessManagerForm(request.POST)
        user_form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            group = Group.objects.get(name='Manager')
            group.user_set.add(user)
            profile_form.instance.user = user
            profile_form.instance.state = request.user.profile.state
            profile = profile_form.save()
            manager = ProcessManager(
                user=user, factory=process_factory)
            manager.save()
            # manager_form.instance.user = user
            # manager = manager_form.save()
            return redirect('mineral:state_admin:manager_list')

    else:
        # manager_form = ProcessManagerForm()
        user_form = UserCreationForm()
        profile_form = ProfileForm()

    context = {
        'title': 'Daftar Pengurus Kilang Proses',
        # 'manager_form': manager_form,
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'mineral/state_admin/manager/form.html', context)


@user_is_jmg_state_admin()
def manager_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    # manager = get_object_or_404(ProcessManager, user=user)
    profile = get_object_or_404(Profile, user=user)
    if request.method == 'POST':
        # manager_form = ProcessManagerForm(request.POST, instance=manager)
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save()
            # manager = manager_form.save()
            return redirect('mineral:state_admin:manager_list')

    else:
        # manager_form = ProcessManagerForm(instance=manager)
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    context = {
        'title': 'Kemaskini Pengurus Kilang Proses',
        # 'manager_form': manager_form,
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'mineral/state_admin/manager/form.html', context)


@user_is_jmg_state_admin()
def manager_choose_operator(request, pk):
    manager = get_object_or_404(ProcessManager, pk=pk)

    context = {
        'manager': manager,
    }

    return render(request, 'mineral/state_admin/manager/choose_operator.html', context)


@user_is_jmg_state_admin()
def manager_add_operator(request, manager_pk, operator_pk):
    manager = get_object_or_404(ProcessManager, pk=manager_pk)

    if request.method == 'POST':
        manager.save()
        return redirect('mineral:state_admin:manager_list')

    return redirect('mineral:state_admin:manager_choose_operator', pk=manager.pk)


@user_is_jmg_state_admin()
def manager_toggle_active(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        if user.is_active == True:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return redirect('mineral:state_admin:manager_list')

    context = {
        'user': user,
    }

    return render(request, 'mineral/state_admin/manager/toggle_active.html', context)


def get_manager_data(request, pk):
    manager = get_object_or_404(ProcessManager, pk=pk)

    data = {
        'process_factory_id': manager.process_factory.id,
        'operator_id': manager.operator.id,
    }

    return JsonResponse(data)


# data views
class DataListView(UserIsJMGStateAdminMixin, ListView):
    template_name = 'mineral/state_admin/data/list.html'
    model = ProcessData
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            state=self.request.user.profile.state,
        )

        id_list = []
        for data in queryset:
            approval = data.get_last_approval()
            if approval:
                if approval.state_approved == True and approval.admin_approved == None:
                    id_list.append(data.id)
        queryset = queryset.filter(id__in=id_list)

        try:
            name = self.request.GET['q']
        except:
            name = ''
        if (name != ''):
            # object_list = queryset.filter(location__icontains=name)
            object_list = queryset
        else:
            object_list = queryset
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Senarai Proses Mineral'
        return context


class DataSuccessListView(UserIsJMGStateAdminMixin, ListView):
    template_name = 'mineral/state_admin/data/success_list.html'
    model = ProcessData
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            state=self.request.user.profile.state,
        )

        id_list = []
        for data in queryset:
            approval = data.get_last_approval()
            if approval:
                if approval.state_approved == True and approval.admin_approved == True:
                    id_list.append(data.id)
        queryset = queryset.filter(id__in=id_list)

        try:
            name = self.request.GET['q']
        except:
            name = ''
        if (name != ''):
            # object_list = queryset.filter(location__icontains=name)
            object_list = queryset
        else:
            object_list = queryset
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Senarai Lulus Proses Mineral'
        return context


@user_is_jmg_state_admin()
def data_detail(request, pk):
    data = get_object_or_404(ProcessData, pk=pk)
    local_operator = get_object_or_404(LocalOperator, data=data)
    local_contractor = get_object_or_404(
        LocalContractor, data=data)
    foreign_operator = get_object_or_404(
        ForeignOperator, data=data)
    foreign_contractor = get_object_or_404(
        ForeignContractor, data=data)
    combustion_machinery = get_object_or_404(
        InternalCombustionMachinery, data=data)
    electric_machinery = get_object_or_404(
        ElectricMachinery, data=data)
    energy_supply = get_object_or_404(EnergySupply, data=data)
    operating_record = get_object_or_404(
        OperatingRecord, data=data)
    other = get_object_or_404(Other, data=data)

    if request.method == 'POST':
        approved = False
        if request.POST.get('choice') == 'yes':
            approved = True

        data_approval = data.get_last_approval()
        data_approval.admin_inspector = request.user
        data_approval.admin_comment = request.POST.get('comment', '')
        data_approval.admin_approved = approved
        data_approval.save()

        # noted here
        # if approved:
        #     jmg_hqs = User.objects.filter(
        #         groups__name='JMG HQ')

        #     notify = Notify()
        #     notify_message = f'{data_approval.requestor} telah menghantar permohonan data untuk kuari "{data.factory}"'
        #     # hq/data_list belum ada
        #     notify_link = reverse('mineral:hq:data_list_success')

        #     for jmg_hq in jmg_hqs:
        #         notify.make_notify(jmg_hq, notify_message, notify_link)

        # else:
        #     miner = data_approval.requestor
        #     state_inspector = data_approval.state_inspector

        #     notify = Notify()
        #     notify_message = f'Data untuk kuari "{data.factory}" telah ditolak'
        #     notify_link = reverse('mineral:data_list')
        #     state_notify_message = f'Data untuk kuari "{data.factory}"({miner}) telah ditolak'

        #     notify.make_notify(miner, notify_message, notify_link)
        #     notify.make_notify(state_inspector, state_notify_message)

        return redirect('mineral:state_admin:data_list')

    context = {
        'title': 'Data Kuari',
        'data': data,
        'local_operator': local_operator,
        'local_contractor': local_contractor,
        'foreign_operator': foreign_operator,
        'foreign_contractor': foreign_contractor,
        'combustion_machinery': combustion_machinery,
        'electric_machinery': electric_machinery,
        'energy_supply': energy_supply,
        'operating_record': operating_record,
        'other': other,
    }

    return render(request, 'mineral/state_admin/data/detail.html', context)


@user_is_jmg_state_admin()
def data_success_detail(request, pk):
    data = get_object_or_404(ProcessData, pk=pk)
    local_operator = get_object_or_404(LocalOperator, data=data)
    local_contractor = get_object_or_404(
        LocalContractor, data=data)
    foreign_operator = get_object_or_404(
        ForeignOperator, data=data)
    foreign_contractor = get_object_or_404(
        ForeignContractor, data=data)
    combustion_machinery = get_object_or_404(
        InternalCombustionMachinery, data=data)
    electric_machinery = get_object_or_404(
        ElectricMachinery, data=data)
    energy_supply = get_object_or_404(EnergySupply, data=data)
    operating_record = get_object_or_404(
        OperatingRecord, data=data)
    other = get_object_or_404(Other, data=data)

    context = {
        'title': 'Data Kuari',
        'data': data,
        'local_operator': local_operator,
        'local_contractor': local_contractor,
        'foreign_operator': foreign_operator,
        'foreign_contractor': foreign_contractor,
        'combustion_machinery': combustion_machinery,
        'electric_machinery': electric_machinery,
        'energy_supply': energy_supply,
        'operating_record': operating_record,
        'other': other,
    }

    return render(request, 'mineral/state_admin/data/success_detail.html', context)
