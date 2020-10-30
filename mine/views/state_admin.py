from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView

from account.models import User
from notification.notify import Notify

from ..models import (
    LeaseHolder,
    Manager,
    Operator,
    Mine,
    MainMineral,
    SideMineral,
    MineMiner,
    MineMinerData,
    MainStatistic,
    LocalOperator,
    LocalContractor,
    ForeignOperator,
    ForeignContractor,
    InternalCombustionMachinery,
    ElectricMachinery,
    EnergySupply,
    OperatingRecord,
)
from ..forms.state_admin import (
    LeaseHolderForm,
    ManagerForm,
    OperatorForm,
    MineForm,
    MainMineralForm,
    SideMineralForm,
    MineMinerForm,
)


# lease holder views
class LeaseHolderListView(ListView):
    template_name = 'mine/state_admin/lease_holder/list.html'
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
        context["title"] = 'Senarai Pemajak Lombong'
        return context


class LeaseHolderCreateView(CreateView):
    template_name = 'mine/state_admin/lease_holder/form.html'
    model = LeaseHolder
    form_class = LeaseHolderForm
    success_url = reverse_lazy('mine:state_admin:lease_holder_list')

    def form_valid(self, form):
        form.instance.state = self.request.user.profile.state
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Tambah Pemajak Lombong'
        return context


class LeaseHolderUpdateView(UpdateView):
    template_name = 'mine/state_admin/lease_holder/form.html'
    model = LeaseHolder
    form_class = LeaseHolderForm
    success_url = reverse_lazy('mine:state_admin:lease_holder_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Update Pemajak Lombong'
        return context


def lease_holder_toggle_active(request, pk):
    lease_holder = get_object_or_404(LeaseHolder, pk=pk)
    if request.method == 'POST':
        if lease_holder.status == True:
            lease_holder.status = False
        else:
            lease_holder.status = True
        lease_holder.save()
        return redirect('mine:state_admin:lease_holder_list')

    context = {
        'lease_holder': lease_holder,
    }

    return render(request, 'mine/state_admin/lease_holder/toggle_active.html', context)


# manager views
class ManagerListView(ListView):
    template_name = 'mine/state_admin/manager/list.html'
    model = Manager
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
        context["title"] = 'Senarai Pengurus Lombong'
        return context


class ManagerCreateView(CreateView):
    template_name = 'mine/state_admin/manager/form.html'
    model = Manager
    form_class = ManagerForm
    success_url = reverse_lazy('mine:state_admin:manager_list')

    def form_valid(self, form):
        form.instance.state = self.request.user.profile.state
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Tambah Pengurus Lombong'
        return context


class ManagerUpdateView(UpdateView):
    template_name = 'mine/state_admin/manager/form.html'
    model = Manager
    form_class = ManagerForm
    success_url = reverse_lazy('mine:state_admin:manager_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Update Pengurus Lombong'
        return context


def manager_toggle_active(request, pk):
    manager = get_object_or_404(Manager, pk=pk)
    if request.method == 'POST':
        if manager.status == True:
            manager.status = False
        else:
            manager.status = True
        manager.save()
        return redirect('mine:state_admin:manager_list')

    context = {
        'manager': manager,
    }

    return render(request, 'mine/state_admin/manager/toggle_active.html', context)


# operator views
class OperatorListView(ListView):
    template_name = 'mine/state_admin/operator/list.html'
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
        context["title"] = 'Senarai Pengusaha Lombong'
        return context


class OperatorCreateView(CreateView):
    template_name = 'mine/state_admin/operator/form.html'
    model = Operator
    form_class = OperatorForm
    success_url = reverse_lazy('mine:state_admin:operator_list')

    def form_valid(self, form):
        form.instance.state = self.request.user.profile.state
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Tambah Pengusaha Lombong'
        return context


class OperatorUpdateView(UpdateView):
    template_name = 'mine/state_admin/operator/form.html'
    model = Operator
    form_class = OperatorForm
    success_url = reverse_lazy('mine:state_admin:operator_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Update Pengusaha Lombong'
        return context


def operator_toggle_active(request, pk):
    operator = get_object_or_404(Operator, pk=pk)
    if request.method == 'POST':
        if operator.status == True:
            operator.status = False
        else:
            operator.status = True
        operator.save()
        return redirect('mine:state_admin:operator_list')

    context = {
        'operator': operator,
    }

    return render(request, 'mine/state_admin/operator/toggle_active.html', context)


# mine views
class MineListView(ListView):
    template_name = 'mine/state_admin/list.html'
    model = Mine
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
        context["title"] = 'Senarai Lombong'
        return context


class MineCreateView(CreateView):
    template_name = 'mine/state_admin/form.html'
    model = Mine
    form_class = MineForm
    success_url = reverse_lazy('mine:state_admin:mineral_list')

    def form_valid(self, form):
        form.instance.state = self.request.user.profile.state
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mine:state_admin:mineral_list', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Tambah Lombong'
        return context


class MineUpdateView(UpdateView):
    template_name = 'mine/state_admin/form.html'
    model = Mine
    form_class = MineForm
    success_url = reverse_lazy('mine:state_admin:mineral_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Update Lombong'
        return context

    def get_success_url(self):
        return reverse('mine:state_admin:mineral_list', kwargs={'pk': self.object.pk})


def toggle_active(request, pk):
    mine = get_object_or_404(Mine, pk=pk)
    if request.method == 'POST':
        if mine.status == True:
            mine.status = False
        else:
            mine.status = True
        mine.save()
        return redirect('mine:state_admin:list')

    context = {
        'mine': mine,
    }

    return render(request, 'mine/state_admin/toggle_active.html', context)


def mine_detail(request, pk):
    mine = get_object_or_404(Mine, pk=pk)
    mine_miner_list = MineMiner.objects.filter(mine=mine)

    try:
        name = request.GET['q']
    except:
        name = ''
    if (name != ''):
        mine_miner_list = mine_miner_list.filter(
            miner__username__icontains=name)

    page = request.GET.get('page', 1)

    paginator = Paginator(mine_miner_list, 10)
    try:
        mine_miner_list = paginator.page(page)
    except PageNotAnInteger:
        mine_miner_list = paginator.page(1)
    except EmptyPage:
        mine_miner_list = paginator.page(paginator.num_pages)

    context = {
        'mine': mine,
        'mine_miner_list': mine_miner_list,
        'title': 'Maklumat Lombong',
    }

    return render(request, 'mine/state_admin/detail.html', context)


def add_miner(request, pk):
    mine = get_object_or_404(Mine, pk=pk)
    user_list = User.objects.all().filter(
        groups__name__in=['Industry'])

    try:
        name = request.GET['q']
    except:
        name = ''
    if (name != ''):
        user_list = user_list.filter(username__icontains=name)

    page = request.GET.get('page', 1)

    paginator = Paginator(user_list, 10)
    try:
        user_list = paginator.page(page)
    except PageNotAnInteger:
        user_list = paginator.page(1)
    except EmptyPage:
        user_list = paginator.page(paginator.num_pages)

    context = {
        'mine': mine,
        'user_list': user_list,
        'title': f'Tambah pengusaha "{mine}"',
    }

    return render(request, 'mine/state_admin/add_user.html', context)


def mine_add_miner(request, mine_pk, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    mine = get_object_or_404(Mine, pk=mine_pk)

    if request.method == 'POST':
        form = MineMinerForm(request.POST)
        if form.is_valid():
            form.instance.miner = user
            form.instance.mine = mine
            form.instance.add_by = request.user
            form.save()

            return redirect('mine:state_admin:detail', mine.pk)

    else:
        form = MineMinerForm()

    context = {
        'each_user': user,
        'mine': mine,
        'form': form,
        'title': f'Tambah pengusaha({user}) ke "{mine}"'
    }

    return render(request, 'mine/state_admin/add_user_form.html', context)


def mine_remove_miner(request, pk):
    mine_miner = get_object_or_404(MineMiner, pk=pk)
    mine_pk = mine_miner.mine.pk
    mine_miner.delete()

    return redirect('mine:state_admin:detail', mine_pk)


def user_mine_list(request, pk):
    user = get_object_or_404(User, pk=pk)
    mine_miner_list = MineMiner.objects.filter(miner=user)

    page = request.GET.get('page', 1)

    paginator = Paginator(mine_miner_list, 10)
    try:
        mine_miner_list = paginator.page(page)
    except PageNotAnInteger:
        mine_miner_list = paginator.page(1)
    except EmptyPage:
        mine_miner_list = paginator.page(paginator.num_pages)

    context = {
        'each_user': user,
        'mine_miner_list': mine_miner_list,
        'title': 'Maklumat Pengguna',
    }

    return render(request, 'mine/state_admin/list_user.html', context)


class MineMinerDataListView(ListView):
    template_name = 'mine/state_admin/miner_data/list.html'
    model = MineMinerData
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
        context["title"] = 'Senarai Data Lombong'
        return context


class MineMinerDataSuccessListView(ListView):
    template_name = 'mine/state_admin/miner_data/list.html'
    model = MineMinerData
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
        context["title"] = 'Senarai Data Lombong'
        return context


def miner_data_detail(request, pk):
    miner_data = get_object_or_404(MineMinerData, pk=pk)
    statistic = get_object_or_404(MainStatistic, miner_data=miner_data)
    local_operator = get_object_or_404(LocalOperator, miner_data=miner_data)
    local_contractor = get_object_or_404(
        LocalContractor, miner_data=miner_data)
    foreign_operator = get_object_or_404(
        ForeignOperator, miner_data=miner_data)
    foreign_contractor = get_object_or_404(
        ForeignContractor, miner_data=miner_data)
    combustion_machinery = get_object_or_404(
        InternalCombustionMachinery, miner_data=miner_data)
    electric_machinery = get_object_or_404(
        ElectricMachinery, miner_data=miner_data)
    energy_supply = get_object_or_404(EnergySupply, miner_data=miner_data)
    operating_record = get_object_or_404(
        OperatingRecord, miner_data=miner_data)

    if request.method == 'POST':
        approved = False
        if request.POST.get('choice') == 'yes':
            approved = True

        data_approval = miner_data.get_last_approval()
        data_approval.admin_inspector = request.user
        data_approval.admin_comment = request.POST.get('comment', '')
        data_approval.admin_approved = approved
        data_approval.save()

        if approved:
            jmg_hqs = User.objects.filter(
                groups__name='JMG HQ')

            notify = Notify()
            notify_message = f'{data_approval.requestor} telah menghantar permohonan data untuk lombong "{miner_data.mine}"'
            # hq/data_list belum ada
            notify_link = reverse('mine:hq:data_list')

            for jmg_hq in jmg_hqs:
                notify.make_notify(jmg_hq, notify_message, notify_link)

        else:
            miner = data_approval.requestor
            state_inspector = data_approval.state_inspector

            notify = Notify()
            notify_message = f'Data untuk lombong "{miner_data.mine}" telah ditolak'
            notify_link = reverse('mine:data_list')
            state_notify_message = f'Data untuk lombong "{miner_data.mine}"({miner}) telah ditolak'

            notify.make_notify(miner, notify_message, notify_link)
            notify.make_notify(state_inspector, state_notify_message)

        return redirect('mine:state_admin:data_list')

    context = {
        'title': 'Data Lombong',
        'miner_data': miner_data,
        'statistic': statistic,
        'local_operator': local_operator,
        'local_contractor': local_contractor,
        'foreign_operator': foreign_operator,
        'foreign_contractor': foreign_contractor,
        'combustion_machinery': combustion_machinery,
        'electric_machinery': electric_machinery,
        'energy_supply': energy_supply,
        'operating_record': operating_record,
    }

    return render(request, 'mine/state_admin/miner_data/detail.html', context=context)


# def miner_data_detail(request, pk):
#     miner_data = get_object_or_404(MineMinerData, pk=pk)
#     next_link = reverse('mine:state_admin:statistic',
#                         kwargs={"pk": miner_data.pk})

#     context = {
#         'title': 'Data Kuari',
#         'miner_data': miner_data,
#         'next_link': next_link,
#     }

#     return render(request, 'mine/state_admin/miner_data/detail.html', context=context)


def statistic_detail(request, pk):
    miner_data = get_object_or_404(MineMinerData, pk=pk)
    prev_link = reverse('mine:state_admin:miner_data',
                        kwargs={"pk": miner_data.pk})
    next_link = reverse('mine:state_admin:local_worker',
                        kwargs={"pk": miner_data.pk})
    statistic = get_object_or_404(MainStatistic, miner_data=miner_data)

    context = {
        'title': 'Perangkaan',
        'statistic': statistic,
        'prev_link': prev_link,
        'next_link': next_link,
    }

    return render(request, 'mine/state_admin/miner_data/statistic/detail.html', context=context)


def local_worker_detail(request, pk):
    miner_data = get_object_or_404(MineMinerData, pk=pk)
    prev_link = reverse('mine:state_admin:statistic',
                        kwargs={"pk": miner_data.pk})
    next_link = reverse('mine:state_admin:foreign_worker',
                        kwargs={"pk": miner_data.pk})
    local_operator = get_object_or_404(LocalOperator, miner_data=miner_data)
    local_contractor = get_object_or_404(
        LocalContractor, miner_data=miner_data)

    context = {
        'title': 'Pekerjaan (Tempatan)',
        'operator': local_operator,
        'contractor': local_contractor,
        'prev_link': prev_link,
        'next_link': next_link,
    }

    return render(request, 'mine/state_admin/miner_data/worker/detail.html', context=context)


def foreign_worker_detail(request, pk):
    miner_data = get_object_or_404(MineMinerData, pk=pk)
    prev_link = reverse('mine:state_admin:local_worker',
                        kwargs={"pk": miner_data.pk})
    next_link = reverse('mine:state_admin:machinery',
                        kwargs={"pk": miner_data.pk})
    foreign_operator = get_object_or_404(
        ForeignOperator, miner_data=miner_data)
    foreign_contractor = get_object_or_404(
        ForeignContractor, miner_data=miner_data)

    context = {
        'title': 'Pekerjaan (Asing)',
        'operator': foreign_operator,
        'contractor': foreign_contractor,
        'prev_link': prev_link,
        'next_link': next_link,
    }

    return render(request, 'mine/state_admin/miner_data/worker/detail.html', context=context)


def machinery_detail(request, pk):
    miner_data = get_object_or_404(MineMinerData, pk=pk)
    prev_link = reverse('mine:state_admin:foreign_worker',
                        kwargs={"pk": miner_data.pk})
    next_link = reverse('mine:state_admin:energy_supply',
                        kwargs={"pk": miner_data.pk})
    combustion_machinery = get_object_or_404(
        InternalCombustionMachinery, miner_data=miner_data)
    electric_machinery = get_object_or_404(
        ElectricMachinery, miner_data=miner_data)

    context = {
        'title': 'Jentera',
        'combustion_machinery': combustion_machinery,
        'electric_machinery': electric_machinery,
        'prev_link': prev_link,
        'next_link': next_link,
    }

    return render(request, 'mine/state_admin/miner_data/machinery/detail.html', context=context)


def energy_supply_detail(request, pk):
    miner_data = get_object_or_404(MineMinerData, pk=pk)
    prev_link = reverse('mine:state_admin:machinery',
                        kwargs={"pk": miner_data.pk})
    next_link = reverse('mine:state_admin:operating_record',
                        kwargs={"pk": miner_data.pk})
    energy_supply = get_object_or_404(EnergySupply, miner_data=miner_data)

    context = {
        'title': 'Bahan Tenaga',
        'energy_supply': energy_supply,
        'prev_link': prev_link,
        'next_link': next_link,
    }

    return render(request, 'mine/state_admin/miner_data/energy_supply/detail.html', context=context)


def operating_record_detail(request, pk):
    miner_data = get_object_or_404(MineMinerData, pk=pk)
    prev_link = reverse('mine:state_admin:energy_supply',
                        kwargs={"pk": miner_data.pk})
    operating_record = get_object_or_404(
        OperatingRecord, miner_data=miner_data)

    if request.method == 'POST':
        approved = False
        if request.POST.get('choice') == 'yes':
            approved = True

        data_approval = miner_data.get_last_approval()
        data_approval.admin_inspector = request.user
        data_approval.admin_comment = request.POST.get('comment', '')
        data_approval.admin_approved = approved
        data_approval.save()

        if approved:
            jmg_hqs = User.objects.filter(
                groups__name='JMG HQ')

            notify = Notify()
            notify_message = f'{data_approval.requestor} telah menghantar permohonan data untuk lombong "{miner_data.mine}"'
            # hq/data_list belum ada
            notify_link = reverse('mine:hq:data_list')

            for jmg_hq in jmg_hqs:
                notify.make_notify(jmg_hq, notify_message, notify_link)

        else:
            miner = data_approval.requestor
            state_inspector = data_approval.state_inspector

            notify = Notify()
            notify_message = f'Data untuk lombong "{miner_data.mine}" telah ditolak'
            notify_link = reverse('mine:data_list')
            state_notify_message = f'Data untuk lombong "{miner_data.mine}"({miner}) telah ditolak'

            notify.make_notify(miner, notify_message, notify_link)
            notify.make_notify(state_inspector, state_notify_message)

        return redirect('mine:state_admin:data_list')

    context = {
        'title': 'Rekod Operasi',
        'operating_record': operating_record,
        'prev_link': prev_link,
        'miner_data_id': miner_data.id,
    }

    return render(request, 'mine/state_admin/miner_data/operating_record/detail.html', context=context)


# mineral views
def mineral_list(request, pk):
    mine = get_object_or_404(Mine, pk=pk)
    main_mineral_list = MainMineral.objects.filter(mine=mine)
    side_mineral_list = SideMineral.objects.filter(mine=mine)

    context = {
        'title': 'Perangkaan',
        'mine': mine,
        'main_mineral_list': main_mineral_list,
        'side_mineral_list': side_mineral_list,
    }

    return render(request, 'mine/state_admin/mineral/list.html', context)


# main mineral views
class MainMineralCreateView(CreateView):
    template_name = 'mine/state_admin/mineral/form.html'
    form_class = MainMineralForm
    model = MainMineral

    def form_valid(self, form):
        self.mine = get_object_or_404(
            Mine, pk=self.kwargs['pk'])
        form.instance.mine = self.mine
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mine:state_admin:mineral_list', kwargs={'pk': self.mine.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Tambah Mineral Utama'
        return context


class MainMineralUpdateView(UpdateView):
    template_name = 'mine/state_admin/mineral/form.html'
    form_class = MainMineralForm
    model = MainMineral

    def get_success_url(self):
        return reverse('mine:state_admin:mineral_list', kwargs={'pk': self.object.mine.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Mineral Utama'
        return context


def main_mineral_delete(request, pk):
    main_mineral = get_object_or_404(MainMineral, pk=pk)
    main_mineral.delete()
    return redirect('mine:state_admin:mineral_list', pk=main_mineral.mine.pk)


# side mineral views
class SideMineralCreateView(CreateView):
    template_name = 'mine/state_admin/mineral/form.html'
    form_class = SideMineralForm
    model = SideMineral

    def form_valid(self, form):
        self.mine = get_object_or_404(
            Mine, pk=self.kwargs['pk'])
        form.instance.mine = self.mine
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mine:state_admin:mineral_list', kwargs={'pk': self.mine.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Tambah Mineral Sampingan'
        return context


class SideMineralUpdateView(UpdateView):
    template_name = 'mine/state_admin/mineral/form.html'
    form_class = SideMineralForm
    model = SideMineral

    def get_success_url(self):
        return reverse('mine:state_admin:mineral_list', kwargs={'pk': self.object.mine.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Mineral Sampingan'
        return context


def side_mineral_delete(request, pk):
    side_mineral = get_object_or_404(SideMineral, pk=pk)
    side_mineral.delete()
    return redirect('mine:state_admin:mineral_list', pk=side_mineral.mine.pk)
