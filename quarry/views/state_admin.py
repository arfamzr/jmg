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
from notification.notify import Notify

from ..models import (
    LeaseHolder,
    QuarryManager,
    Operator,
    Quarry,
    Lot,
    MainRock,
    SideRock,
    Data,
    SalesSubmission,
    LocalFinalUses,
    ExportFinalUses,
    LocalOperator,
    LocalContractor,
    ForeignOperator,
    ForeignContractor,
    InternalCombustionMachinery,
    ElectricMachinery,
    DailyExplosive,
    EnergySupply,
    OperatingRecord,
    Royalties,
    Other,
    Approval,
)
from ..forms.state_admin import (
    LeaseHolderForm,
    QuarryManagerForm,
    OperatorForm,
    QuarryOwnerForm,
    QuarryForm,
    LotForm,
    MainRockForm,
    SideRockForm,
)


# lease holder views
class LeaseHolderListView(ListView):
    template_name = 'quarry/state_admin/lease_holder/list.html'
    model = LeaseHolder
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
        context["title"] = 'Senarai Pemajak Kuari'
        return context


class LeaseHolderCreateView(CreateView):
    template_name = 'quarry/state_admin/lease_holder/form.html'
    model = LeaseHolder
    form_class = LeaseHolderForm
    success_url = reverse_lazy('quarry:state_admin:lease_holder_list')

    def form_valid(self, form):
        form.instance.state = self.request.user.profile.state
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Tambah Pemajak Kuari'
        return context


class LeaseHolderUpdateView(UpdateView):
    template_name = 'quarry/state_admin/lease_holder/form.html'
    model = LeaseHolder
    form_class = LeaseHolderForm
    success_url = reverse_lazy('quarry:state_admin:lease_holder_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Update Pemajak Kuari'
        return context


def lease_holder_toggle_active(request, pk):
    lease_holder = get_object_or_404(LeaseHolder, pk=pk)
    if request.method == 'POST':
        if lease_holder.status == True:
            lease_holder.status = False
        else:
            lease_holder.status = True
        lease_holder.save()
        return redirect('quarry:state_admin:lease_holder_list')

    context = {
        'lease_holder': lease_holder,
    }

    return render(request, 'quarry/state_admin/lease_holder/toggle_active.html', context)


# manager views
class ManagerListView(ListView):
    template_name = 'quarry/state_admin/manager/list.html'
    model = QuarryManager
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
        context["title"] = 'Senarai Pengurus Kuari'
        return context


def manager_create(request, pk):
    lease_holder = get_object_or_404(LeaseHolder, pk=pk)
    if request.method == 'POST':
        # manager_form = QuarryManagerForm(request.POST)
        user_form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            group = Group.objects.get(name='Manager')
            group.user_set.add(user)
            profile_form.instance.user = user
            profile_form.instance.state = request.user.profile.state
            profile = profile_form.save()
            manager = QuarryManager(user=user, lease_holder=lease_holder)
            manager.save()
            # manager_form.instance.user = user
            # manager = manager_form.save()
            return redirect('quarry:state_admin:manager_list')

    else:
        # manager_form = QuarryManagerForm()
        user_form = UserCreationForm()
        profile_form = ProfileForm()

    context = {
        'title': 'Daftar Pengurus Kuari',
        # 'manager_form': manager_form,
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'quarry/state_admin/manager/form.html', context)


def manager_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    # manager = get_object_or_404(QuarryManager, user=user)
    profile = get_object_or_404(Profile, user=user)
    if request.method == 'POST':
        # manager_form = QuarryManagerForm(request.POST, instance=manager)
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save()
            # manager = manager_form.save()
            return redirect('quarry:state_admin:manager_list')

    else:
        # manager_form = QuarryManagerForm(instance=manager)
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    context = {
        'title': 'Update Pengurus Kuari',
        # 'manager_form': manager_form,
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'quarry/state_admin/manager/form.html', context)


def manager_choose_operator(request, pk):
    manager = get_object_or_404(QuarryManager, pk=pk)
    operator_list = Operator.objects.filter(state=request.user.profile.state)

    context = {
        'manager': manager,
        'operator_list': operator_list,
    }

    return render(request, 'quarry/state_admin/manager/choose_operator.html', context)


def manager_add_operator(request, manager_pk, operator_pk):
    manager = get_object_or_404(QuarryManager, pk=manager_pk)
    operator = get_object_or_404(Operator, pk=operator_pk)

    if request.method == 'POST':
        manager.operator = operator
        manager.save()
        return redirect('quarry:state_admin:manager_list')

    return redirect('quarry:state_admin:manager_choose_operator', pk=manager.pk)


def manager_toggle_active(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        if user.is_active == True:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return redirect('quarry:state_admin:manager_list')

    context = {
        'user': user,
    }

    return render(request, 'quarry/state_admin/manager/toggle_active.html', context)


def get_manager_data(request, pk):
    manager = get_object_or_404(QuarryManager, pk=pk)

    data = {
        'lease_holder_id': manager.lease_holder.id,
        'operator_id': manager.operator.id,
    }

    return JsonResponse(data)


# operator views
class OperatorListView(ListView):
    template_name = 'quarry/state_admin/operator/list.html'
    model = Operator
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
        context["title"] = 'Senarai Pengusaha Kuari'
        return context


class OperatorCreateView(CreateView):
    template_name = 'quarry/state_admin/operator/form.html'
    model = Operator
    form_class = OperatorForm
    success_url = reverse_lazy('quarry:state_admin:operator_list')

    def form_valid(self, form):
        form.instance.state = self.request.user.profile.state
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Tambah Pengusaha Kuari'
        return context


class OperatorUpdateView(UpdateView):
    template_name = 'quarry/state_admin/operator/form.html'
    model = Operator
    form_class = OperatorForm
    success_url = reverse_lazy('quarry:state_admin:operator_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Update Pengusaha Kuari'
        return context


def operator_toggle_active(request, pk):
    operator = get_object_or_404(Operator, pk=pk)
    if request.method == 'POST':
        if operator.status == True:
            operator.status = False
        else:
            operator.status = True
        operator.save()
        return redirect('quarry:state_admin:operator_list')

    context = {
        'operator': operator,
    }

    return render(request, 'quarry/state_admin/operator/toggle_active.html', context)


# quarry views
class QuarryListView(ListView):
    template_name = 'quarry/state_admin/list.html'
    model = Quarry
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
            object_list = queryset.filter(location__icontains=name)
        else:
            object_list = queryset
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Senarai Kuari'
        return context


class QuarryCreateView(CreateView):
    template_name = 'quarry/state_admin/form.html'
    model = Quarry
    form_class = QuarryForm

    def dispatch(self, request, *args, **kwargs):
        self.manager = get_object_or_404(QuarryManager, pk=self.kwargs['pk'])
        self.operator = self.manager.operator
        self.lease_holder = self.manager.lease_holder
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.lease_holder = self.lease_holder
        form.instance.manager = self.manager
        form.instance.operator = self.operator
        form.instance.state = self.request.user.profile.state
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('quarry:state_admin:lot_list', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Tambah Kuari'
        context['owner_form'] = QuarryOwnerForm(initial={
            'lease_holder': self.lease_holder,
            'manager': self.manager,
            'operator': self.operator,
        })
        return context


class QuarryUpdateView(UpdateView):
    template_name = 'quarry/state_admin/form.html'
    model = Quarry
    form_class = QuarryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Update Kuari'
        context['owner_form'] = QuarryOwnerForm(initial={
            'lease_holder': self.object.lease_holder,
            'manager': self.object.manager,
            'operator': self.object.operator,
        })
        return context

    def get_success_url(self):
        return reverse('quarry:state_admin:lot_list', kwargs={'pk': self.object.pk})


def toggle_active(request, pk):
    quarry = get_object_or_404(Quarry, pk=pk)
    if request.method == 'POST':
        if quarry.status == True:
            quarry.status = False
        else:
            quarry.status = True
        quarry.save()
        return redirect('quarry:state_admin:list')

    context = {
        'quarry': quarry,
    }

    return render(request, 'quarry/state_admin/toggle_active.html', context)


def quarry_detail(request, pk):
    quarry = get_object_or_404(Quarry, pk=pk)

    context = {
        'quarry': quarry,
        'title': 'Maklumat Quarry',
    }

    return render(request, 'quarry/state_admin/detail.html', context)


# lot views
def lot_list(request, pk):
    quarry = get_object_or_404(Quarry, pk=pk)
    lot_list = Lot.objects.filter(quarry=quarry)

    context = {
        'title': 'Batuan',
        'quarry': quarry,
        'lot_list': lot_list,
    }

    return render(request, 'quarry/state_admin/lot/list.html', context)


class LotCreateView(CreateView):
    template_name = 'quarry/state_admin/lot/form.html'
    form_class = LotForm
    model = Lot

    def form_valid(self, form):
        self.quarry = get_object_or_404(
            Quarry, pk=self.kwargs['pk'])
        form.instance.quarry = self.quarry
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('quarry:state_admin:lot_list', kwargs={'pk': self.quarry.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Tambah Lot'
        return context


class LotUpdateView(UpdateView):
    template_name = 'quarry/state_admin/lot/form.html'
    form_class = LotForm
    model = Lot

    def get_success_url(self):
        return reverse('quarry:state_admin:lot_list', kwargs={'pk': self.object.quarry.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Lot'
        return context


def lot_delete(request, pk):
    lot = get_object_or_404(Lot, pk=pk)
    if request.method == 'POST':
        lot.delete()
    return redirect('quarry:state_admin:lot_list', pk=lot.quarry.pk)


# rock views
def rock_list(request, pk):
    quarry = get_object_or_404(Quarry, pk=pk)
    main_rock_list = MainRock.objects.filter(quarry=quarry)
    side_rock_list = SideRock.objects.filter(quarry=quarry)

    context = {
        'title': 'Batuan',
        'quarry': quarry,
        'main_rock_list': main_rock_list,
        'side_rock_list': side_rock_list,
    }

    return render(request, 'quarry/state_admin/rock/list.html', context)


# main rock views
class MainRockCreateView(CreateView):
    template_name = 'quarry/state_admin/rock/form.html'
    form_class = MainRockForm
    model = MainRock

    def form_valid(self, form):
        self.quarry = get_object_or_404(
            Quarry, pk=self.kwargs['pk'])
        form.instance.quarry = self.quarry
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('quarry:state_admin:rock_list', kwargs={'pk': self.quarry.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Tambah Batuan Utama'
        return context


class MainRockUpdateView(UpdateView):
    template_name = 'quarry/state_admin/rock/form.html'
    form_class = MainRockForm
    model = MainRock

    def get_success_url(self):
        return reverse('quarry:state_admin:rock_list', kwargs={'pk': self.object.quarry.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Batuan Utama'
        return context


def main_rock_delete(request, pk):
    main_rock = get_object_or_404(MainRock, pk=pk)
    if request.method == 'POST':
        main_rock.delete()
    return redirect('quarry:state_admin:rock_list', pk=main_rock.quarry.pk)


# side rock views
class SideRockCreateView(CreateView):
    template_name = 'quarry/state_admin/rock/form.html'
    form_class = SideRockForm
    model = SideRock

    def form_valid(self, form):
        self.quarry = get_object_or_404(
            Quarry, pk=self.kwargs['pk'])
        form.instance.quarry = self.quarry
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('quarry:state_admin:rock_list', kwargs={'pk': self.quarry.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Tambah Batuan Sampingan'
        return context


class SideRockUpdateView(UpdateView):
    template_name = 'quarry/state_admin/rock/form.html'
    form_class = SideRockForm
    model = SideRock

    def get_success_url(self):
        return reverse('quarry:state_admin:rock_list', kwargs={'pk': self.object.quarry.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Batuan Sampingan'
        return context


def side_rock_delete(request, pk):
    side_rock = get_object_or_404(SideRock, pk=pk)
    if request.method == 'POST':
        side_rock.delete()
    return redirect('quarry:state_admin:rock_list', pk=side_rock.quarry.pk)


# data views
class DataListView(ListView):
    template_name = 'quarry/state_admin/data/list.html'
    model = Data
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
        context["title"] = 'Senarai PKB'
        return context


class DataSuccessListView(ListView):
    template_name = 'quarry/state_admin/data/success_list.html'
    model = Data
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
        context["title"] = 'Senarai Lulus PKB'
        return context


def data_detail(request, pk):
    data = get_object_or_404(Data, pk=pk)
    local_final_uses = get_object_or_404(LocalFinalUses, data=data)
    export_final_uses = get_object_or_404(
        ExportFinalUses, data=data)
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
    daily_explosive = get_object_or_404(DailyExplosive, data=data)
    energy_supply = get_object_or_404(EnergySupply, data=data)
    operating_record = get_object_or_404(
        OperatingRecord, data=data)
    royalties = get_object_or_404(Royalties, data=data)
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

        if approved:
            jmg_hqs = User.objects.filter(
                groups__name='JMG HQ')

            notify = Notify()
            notify_message = f'{data_approval.requestor} telah menghantar permohonan data untuk kuari "{data.quarry}"'
            # hq/data_list belum ada
            notify_link = reverse('quarry:hq:data_list')

            for jmg_hq in jmg_hqs:
                notify.make_notify(jmg_hq, notify_message, notify_link)

        else:
            miner = data_approval.requestor
            state_inspector = data_approval.state_inspector

            notify = Notify()
            notify_message = f'Data untuk kuari "{data.quarry}" telah ditolak'
            notify_link = reverse('quarry:data_list')
            state_notify_message = f'Data untuk kuari "{data.quarry}"({miner}) telah ditolak'

            notify.make_notify(miner, notify_message, notify_link)
            notify.make_notify(state_inspector, state_notify_message)

        return redirect('quarry:state_admin:data_list')

    context = {
        'title': 'Data Kuari',
        'data': data,
        'local_final_uses': local_final_uses,
        'export_final_uses': export_final_uses,
        'local_operator': local_operator,
        'local_contractor': local_contractor,
        'foreign_operator': foreign_operator,
        'foreign_contractor': foreign_contractor,
        'combustion_machinery': combustion_machinery,
        'electric_machinery': electric_machinery,
        'daily_explosive': daily_explosive,
        'energy_supply': energy_supply,
        'operating_record': operating_record,
        'royalties': royalties,
        'other': other,
    }

    return render(request, 'quarry/state_admin/data/detail.html', context)


def data_success_detail(request, pk):
    data = get_object_or_404(Data, pk=pk)
    local_final_uses = get_object_or_404(LocalFinalUses, data=data)
    export_final_uses = get_object_or_404(
        ExportFinalUses, data=data)
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
    daily_explosive = get_object_or_404(DailyExplosive, data=data)
    energy_supply = get_object_or_404(EnergySupply, data=data)
    operating_record = get_object_or_404(
        OperatingRecord, data=data)
    royalties = get_object_or_404(Royalties, data=data)
    other = get_object_or_404(Other, data=data)

    context = {
        'title': 'Data Kuari',
        'data': data,
        'local_final_uses': local_final_uses,
        'export_final_uses': export_final_uses,
        'local_operator': local_operator,
        'local_contractor': local_contractor,
        'foreign_operator': foreign_operator,
        'foreign_contractor': foreign_contractor,
        'combustion_machinery': combustion_machinery,
        'electric_machinery': electric_machinery,
        'daily_explosive': daily_explosive,
        'energy_supply': energy_supply,
        'operating_record': operating_record,
        'royalties': royalties,
        'other': other,
    }

    return render(request, 'quarry/state_admin/data/success_detail.html', context)


# def quarry_detail(request, pk):
#     quarry = get_object_or_404(Quarry, pk=pk)
#     quarry_miner_list = QuarryMiner.objects.filter(quarry=quarry)

#     try:
#         name = request.GET['q']
#     except:
#         name = ''
#     if (name != ''):
#         quarry_miner_list = quarry_miner_list.filter(
#             miner__username__icontains=name)

#     page = request.GET.get('page', 1)

#     paginator = Paginator(quarry_miner_list, 10)
#     try:
#         quarry_miner_list = paginator.page(page)
#     except PageNotAnInteger:
#         quarry_miner_list = paginator.page(1)
#     except EmptyPage:
#         quarry_miner_list = paginator.page(paginator.num_pages)

#     context = {
#         'quarry': quarry,
#         'quarry_miner_list': quarry_miner_list,
#         'title': 'Maklumat Kuari',
#     }

#     return render(request, 'quarry/state_admin/detail.html', context)


# def add_miner(request, pk):
#     quarry = get_object_or_404(Quarry, pk=pk)
#     user_list = User.objects.all().filter(
#         groups__name__in=['Industry'])

#     try:
#         name = request.GET['q']
#     except:
#         name = ''
#     if (name != ''):
#         user_list = user_list.filter(username__icontains=name)

#     context = {
#         'quarry': quarry,
#         'user_list': user_list,
#         'title': f'Tambah pengusaha "{quarry}"',
#     }

#     return render(request, 'quarry/state_admin/add_user.html', context)


# def quarry_add_miner(request, quarry_pk, user_pk):
#     user = get_object_or_404(User, pk=user_pk)
#     quarry = get_object_or_404(Quarry, pk=quarry_pk)

#     if request.method == 'POST':
#         form = QuarryMinerForm(request.POST)
#         if form.is_valid():
#             form.instance.miner = user
#             form.instance.quarry = quarry
#             form.instance.add_by = request.user
#             form.save()

#             return redirect('quarry:state_admin:detail', quarry.pk)

#     else:
#         form = QuarryMinerForm()

#     context = {
#         'each_user': user,
#         'quarry': quarry,
#         'form': form,
#         'title': f'Tambah pengusaha({user}) ke "{quarry}"'
#     }

#     return render(request, 'quarry/state_admin/add_user_form.html', context)


# def quarry_remove_miner(request, pk):
#     quarry_miner = get_object_or_404(QuarryMiner, pk=pk)
#     quarry_pk = quarry_miner.quarry.pk
#     quarry_miner.delete()

#     return redirect('quarry:state_admin:detail', quarry_pk)


# def user_quarry_list(request, pk):
#     user = get_object_or_404(User, pk=pk)
#     quarry_miner_list = QuarryMiner.objects.filter(miner=user)

#     page = request.GET.get('page', 1)

#     paginator = Paginator(quarry_miner_list, 10)
#     try:
#         quarry_miner_list = paginator.page(page)
#     except PageNotAnInteger:
#         quarry_miner_list = paginator.page(1)
#     except EmptyPage:
#         quarry_miner_list = paginator.page(paginator.num_pages)

#     context = {
#         'each_user': user,
#         'quarry_miner_list': quarry_miner_list,
#         'title': 'Maklumat Pengguna',
#     }

#     return render(request, 'quarry/state_admin/list_user.html', context)


# def data_detail(request, pk):
#     data = get_object_or_404(QuarryMinerData, pk=pk)
#     next_link = reverse('quarry:state_admin:production_statistic',
#                         kwargs={"pk": data.pk})

#     context = {
#         'title': 'Data Kuari',
#         'data': data,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/state_admin/data/detail.html', context=context)


# def production_statistic_detail(request, pk):
#     data = get_object_or_404(QuarryMinerData, pk=pk)
#     prev_link = reverse('quarry:state_admin:data',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('quarry:state_admin:sales_submission',
#                         kwargs={"pk": data.pk})
#     production_statistic = get_object_or_404(
#         ProductionStatistic, data=data)

#     context = {
#         'title': 'Perangkaan Pengeluaran',
#         'production_statistic': production_statistic,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/state_admin/data/production_statistic/detail.html', context=context)


# def sales_submission_detail(request, pk):
#     data = get_object_or_404(QuarryMinerData, pk=pk)
#     prev_link = reverse('quarry:state_admin:production_statistic',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('quarry:state_admin:final_uses',
#                         kwargs={"pk": data.pk})
#     sales_submission = get_object_or_404(
#         SalesSubmission, data=data)

#     context = {
#         'title': 'Penyerahan Jualan',
#         'sales_submission': sales_submission,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/state_admin/data/sales_submission/detail.html', context=context)


# def final_uses_detail(request, pk):
#     data = get_object_or_404(QuarryMinerData, pk=pk)
#     prev_link = reverse('quarry:state_admin:sales_submission',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('quarry:state_admin:local_worker',
#                         kwargs={"pk": data.pk})
#     local_final_uses = get_object_or_404(LocalFinalUses, data=data)
#     export_final_uses = get_object_or_404(
#         ExportFinalUses, data=data)

#     context = {
#         'title': 'Kegunaan Akhir',
#         'local_final_uses': local_final_uses,
#         'export_final_uses': export_final_uses,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/state_admin/data/final_uses/detail.html', context=context)


# def local_worker_detail(request, pk):
#     data = get_object_or_404(QuarryMinerData, pk=pk)
#     prev_link = reverse('quarry:state_admin:final_uses',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('quarry:state_admin:foreign_worker',
#                         kwargs={"pk": data.pk})
#     local_operator = get_object_or_404(LocalOperator, data=data)
#     local_contractor = get_object_or_404(
#         LocalContractor, data=data)

#     context = {
#         'title': 'Pekerjaan (Tempatan)',
#         'operator': local_operator,
#         'contractor': local_contractor,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/state_admin/data/worker/detail.html', context=context)


# def foreign_worker_detail(request, pk):
#     data = get_object_or_404(QuarryMinerData, pk=pk)
#     prev_link = reverse('quarry:state_admin:local_worker',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('quarry:state_admin:machinery',
#                         kwargs={"pk": data.pk})
#     foreign_operator = get_object_or_404(
#         ForeignOperator, data=data)
#     foreign_contractor = get_object_or_404(
#         ForeignContractor, data=data)

#     context = {
#         'title': 'Pekerjaan (Asing)',
#         'operator': foreign_operator,
#         'contractor': foreign_contractor,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/state_admin/data/worker/detail.html', context=context)


# def machinery_detail(request, pk):
#     data = get_object_or_404(QuarryMinerData, pk=pk)
#     prev_link = reverse('quarry:state_admin:foreign_worker',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('quarry:state_admin:daily_explosive',
#                         kwargs={"pk": data.pk})
#     combustion_machinery = get_object_or_404(
#         InternalCombustionMachinery, data=data)
#     electric_machinery = get_object_or_404(
#         ElectricMachinery, data=data)

#     context = {
#         'title': 'Jentera',
#         'combustion_machinery': combustion_machinery,
#         'electric_machinery': electric_machinery,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/state_admin/data/machinery/detail.html', context=context)


# def daily_explosive_detail(request, pk):
#     data = get_object_or_404(QuarryMinerData, pk=pk)
#     prev_link = reverse('quarry:state_admin:machinery',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('quarry:state_admin:energy_supply',
#                         kwargs={"pk": data.pk})
#     daily_explosive = get_object_or_404(DailyExplosive, data=data)

#     context = {
#         'title': 'Bahan Letupan Harian',
#         'daily_explosive': daily_explosive,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/state_admin/data/daily_explosive/detail.html', context=context)


# def energy_supply_detail(request, pk):
#     data = get_object_or_404(QuarryMinerData, pk=pk)
#     prev_link = reverse('quarry:state_admin:daily_explosive',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('quarry:state_admin:operating_record',
#                         kwargs={"pk": data.pk})
#     energy_supply = get_object_or_404(EnergySupply, data=data)

#     context = {
#         'title': 'Bahan Tenaga',
#         'energy_supply': energy_supply,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/state_admin/data/energy_supply/detail.html', context=context)


# def operating_record_detail(request, pk):
#     data = get_object_or_404(QuarryMinerData, pk=pk)
#     prev_link = reverse('quarry:state_admin:energy_supply',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('quarry:state_admin:royalties',
#                         kwargs={"pk": data.pk})
#     operating_record = get_object_or_404(
#         OperatingRecord, data=data)

#     context = {
#         'title': 'Rekod Operasi',
#         'operating_record': operating_record,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/state_admin/data/operating_record/detail.html', context=context)


# def royalties_detail(request, pk):
#     data = get_object_or_404(QuarryMinerData, pk=pk)
#     prev_link = reverse('quarry:state_admin:operating_record',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('quarry:state_admin:other',
#                         kwargs={"pk": data.pk})
#     royalties = get_object_or_404(Royalties, data=data)

#     context = {
#         'title': 'Royalti',
#         'royalties': royalties,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/state_admin/data/royalties/detail.html', context=context)


# def other_detail(request, pk):
#     data = get_object_or_404(QuarryMinerData, pk=pk)
#     prev_link = reverse('quarry:state_admin:royalties',
#                         kwargs={"pk": data.pk})
#     other = get_object_or_404(Other, data=data)

#     if request.method == 'POST':
#         approved = False
#         if request.POST.get('choice') == 'yes':
#             approved = True

#         data_approval = data.get_last_approval()
#         data_approval.admin_inspector = request.user
#         data_approval.admin_comment = request.POST.get('comment', '')
#         data_approval.admin_approved = approved
#         data_approval.save()

#         if approved:
#             jmg_hqs = User.objects.filter(
#                 groups__name='JMG HQ')

#             notify = Notify()
#             notify_message = f'{data_approval.requestor} telah menghantar permohonan data untuk kuari "{data.quarry}"'
#             # hq/data_list belum ada
#             notify_link = reverse('quarry:hq:data_list')

#             for jmg_hq in jmg_hqs:
#                 notify.make_notify(jmg_hq, notify_message, notify_link)

#         else:
#             miner = data_approval.requestor
#             state_inspector = data_approval.state_inspector

#             notify = Notify()
#             notify_message = f'Data untuk kuari "{data.quarry}" telah ditolak'
#             notify_link = reverse('quarry:data_list')
#             state_notify_message = f'Data untuk kuari "{data.quarry}"({miner}) telah ditolak'

#             notify.make_notify(miner, notify_message, notify_link)
#             notify.make_notify(state_inspector, state_notify_message)

#         return redirect('quarry:state_admin:data_list')

#     context = {
#         'title': 'Lain-lain',
#         'other': other,
#         'prev_link': prev_link,
#         'data_id': data.id,
#     }

#     return render(request, 'quarry/state_admin/data/other/detail.html', context=context)


# def quarry_graph(request, pk):
#     data = get_object_or_404(QuarryMinerData, pk=pk)
#     rock_type = data.quarry.main_rock_type
#     rock_list = QuarryDataApproval.objects.filter(data=data)

#     def get_rock_list(rock_list):
#         rock_jan_list = rock_list.filter(
#             data__month=1)
#         rock_jan_production = 0
#         rock_jan_royalties = 0
#         for rock in rock_jan_list:
#             rock_jan_production += rock.data.productionstatistic.main_rock_production
#             rock_jan_royalties += rock.data.royalties.royalties

#         rock_feb_list = rock_list.filter(
#             data__month=2)
#         rock_feb_production = 0
#         rock_feb_royalties = 0
#         for rock in rock_feb_list:
#             rock_feb_production += rock.data.productionstatistic.main_rock_production
#             rock_feb_royalties += rock.data.royalties.royalties

#         rock_mac_list = rock_list.filter(
#             data__month=3)
#         rock_mac_production = 0
#         rock_mac_royalties = 0
#         for rock in rock_mac_list:
#             rock_mac_production += rock.data.productionstatistic.main_rock_production
#             rock_mac_royalties += rock.data.royalties.royalties

#         rock_apr_list = rock_list.filter(
#             data__month=4)
#         rock_apr_production = 0
#         rock_apr_royalties = 0
#         for rock in rock_apr_list:
#             rock_apr_production += rock.data.productionstatistic.main_rock_production
#             rock_apr_royalties += rock.data.royalties.royalties

#         rock_mei_list = rock_list.filter(
#             data__month=5)
#         rock_mei_production = 0
#         rock_mei_royalties = 0
#         for rock in rock_mei_list:
#             rock_mei_production += rock.data.productionstatistic.main_rock_production
#             rock_mei_royalties += rock.data.royalties.royalties

#         rock_jun_list = rock_list.filter(
#             data__month=6)
#         rock_jun_production = 0
#         rock_jun_royalties = 0
#         for rock in rock_jun_list:
#             rock_jun_production += rock.data.productionstatistic.main_rock_production
#             rock_jun_royalties += rock.data.royalties.royalties

#         rock_jul_list = rock_list.filter(
#             data__month=7)
#         rock_jul_production = 0
#         rock_jul_royalties = 0
#         for rock in rock_jul_list:
#             rock_jul_production += rock.data.productionstatistic.main_rock_production
#             rock_jul_royalties += rock.data.royalties.royalties

#         rock_ogos_list = rock_list.filter(
#             data__month=8)
#         rock_ogos_production = 0
#         rock_ogos_royalties = 0
#         for rock in rock_ogos_list:
#             rock_ogos_production += rock.data.productionstatistic.main_rock_production
#             rock_ogos_royalties += rock.data.royalties.royalties

#         rock_sep_list = rock_list.filter(
#             data__month=9)
#         rock_sep_production = 0
#         rock_sep_royalties = 0
#         for rock in rock_sep_list:
#             rock_sep_production += rock.data.productionstatistic.main_rock_production
#             rock_sep_royalties += rock.data.royalties.royalties

#         rock_okt_list = rock_list.filter(
#             data__month=10)
#         rock_okt_production = 0
#         rock_okt_royalties = 0
#         for rock in rock_okt_list:
#             rock_okt_production += rock.data.productionstatistic.main_rock_production
#             rock_okt_royalties += rock.data.royalties.royalties

#         rock_nov_list = rock_list.filter(
#             data__month=11)
#         rock_nov_production = 0
#         rock_nov_royalties = 0
#         for rock in rock_nov_list:
#             rock_nov_production += rock.data.productionstatistic.main_rock_production
#             rock_nov_royalties += rock.data.royalties.royalties

#         rock_dis_list = rock_list.filter(
#             data__month=12)
#         rock_dis_production = 0
#         rock_dis_royalties = 0
#         for rock in rock_dis_list:
#             rock_dis_production += rock.data.productionstatistic.main_rock_production
#             rock_dis_royalties += rock.data.royalties.royalties

#         rock = {
#             'jan': {
#                 'production': rock_jan_production,
#                 'royalties': rock_jan_royalties,
#             },
#             'feb': {
#                 'production': rock_feb_production,
#                 'royalties': rock_feb_royalties,
#             },
#             'mac': {
#                 'production': rock_mac_production,
#                 'royalties': rock_mac_royalties,
#             },
#             'apr': {
#                 'production': rock_apr_production,
#                 'royalties': rock_apr_royalties,
#             },
#             'mei': {
#                 'production': rock_mei_production,
#                 'royalties': rock_mei_royalties,
#             },
#             'jun': {
#                 'production': rock_jun_production,
#                 'royalties': rock_jun_royalties,
#             },
#             'jul': {
#                 'production': rock_jul_production,
#                 'royalties': rock_jul_royalties,
#             },
#             'ogos': {
#                 'production': rock_ogos_production,
#                 'royalties': rock_ogos_royalties,
#             },
#             'sep': {
#                 'production': rock_sep_production,
#                 'royalties': rock_sep_royalties,
#             },
#             'okt': {
#                 'production': rock_okt_production,
#                 'royalties': rock_okt_royalties,
#             },
#             'nov': {
#                 'production': rock_nov_production,
#                 'royalties': rock_nov_royalties,
#             },
#             'dis': {
#                 'production': rock_dis_production,
#                 'royalties': rock_dis_royalties,
#             },
#         }

#         return rock

#     rock = get_rock_list(rock_list)

#     months = [
#         {
#             'name': 'JANUARI',
#             'rock': rock['jan'],
#         },
#         {
#             'name': 'FEBRUARI',
#             'rock': rock['feb'],
#         },
#         {
#             'name': 'MAC',
#             'rock': rock['mac'],
#         },
#         {
#             'name': 'APRIL',
#             'rock': rock['apr'],
#         },
#         {
#             'name': 'MEI',
#             'rock': rock['mei'],
#         },
#         {
#             'name': 'JUN',
#             'rock': rock['jun'],
#         },
#         {
#             'name': 'JULAI',
#             'rock': rock['jul'],
#         },
#         {
#             'name': 'OGOS',
#             'rock': rock['ogos'],
#         },
#         {
#             'name': 'SEPTEMBER',
#             'rock': rock['sep'],
#         },
#         {
#             'name': 'OKTOBER',
#             'rock': rock['okt'],
#         },
#         {
#             'name': 'NOVEMBER',
#             'rock': rock['nov'],
#         },
#         {
#             'name': 'DISEMBER',
#             'rock': rock['dis'],
#         },
#     ]

#     rocks = {
#         'name': rock_type,
#         'production': sum([month['rock']['production'] for month in months]),
#         'royalties': sum([month['rock']['royalties'] for month in months]),
#     }

#     context = {
#         'title': 'Laporan/Graph Kuari',
#         'rock': rocks,
#         'months': months,
#     }

#     return render(request, 'quarry/state_admin/graph/data.html', context)
