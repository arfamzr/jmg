from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView

from account.models import User
from notification.notify import Notify

from ..models import (
    Mine,
    Data,
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


# data views
class DataListView(ListView):
    template_name = 'mine/state/data/list.html'
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
                if approval.state_approved == None:
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
        context["title"] = 'Senarai RPLB'
        return context


def data_detail(request, pk):
    data = get_object_or_404(Data, pk=pk)
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

    if request.method == 'POST':
        approved = False
        if request.POST.get('choice') == 'yes':
            approved = True

        data_approval = data.get_last_approval()
        data_approval.state_inspector = request.user
        data_approval.state_comment = request.POST.get('comment', '')
        data_approval.state_approved = approved
        data_approval.save()

        if approved:
            jmg_state_admins = User.objects.filter(
                groups__name='JMG State Admin', profile__state=data.state)

            notify = Notify()
            notify_message = f'{data_approval.requestor} telah menghantar permohonan data untuk kuari "{data.mine}"'
            notify_link = reverse('mine:state_admin:data_list')

            for jmg_state_admin in jmg_state_admins:
                notify.make_notify(
                    jmg_state_admin, notify_message, notify_link)
        else:
            miner = data_approval.requestor

            notify = Notify()
            notify_message = f'RPLB "{data.mine}" telah ditolak'
            notify_link = reverse('mine:data_list')

            notify.make_notify(miner, notify_message, notify_link)

        return redirect('mine:state:data_list')

    context = {
        'title': 'Data RPLB',
        'data': data,
        'local_operator': local_operator,
        'local_contractor': local_contractor,
        'foreign_operator': foreign_operator,
        'foreign_contractor': foreign_contractor,
        'combustion_machinery': combustion_machinery,
        'electric_machinery': electric_machinery,
        'energy_supply': energy_supply,
        'operating_record': operating_record,
    }

    return render(request, 'mine/state/data/detail.html', context=context)


# mine view
class MineListView(ListView):
    template_name = 'mine/state/list.html'
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


# def mine_detail(request, pk):
#     mine = get_object_or_404(Mine, pk=pk)
#     mine_miner_list = MineMiner.objects.filter(mine=mine)

#     try:
#         name = request.GET['q']
#     except:
#         name = ''
#     if (name != ''):
#         mine_miner_list = mine_miner_list.filter(
#             miner__username__icontains=name)

#     page = request.GET.get('page', 1)

#     paginator = Paginator(mine_miner_list, 10)
#     try:
#         mine_miner_list = paginator.page(page)
#     except PageNotAnInteger:
#         mine_miner_list = paginator.page(1)
#     except EmptyPage:
#         mine_miner_list = paginator.page(paginator.num_pages)

#     context = {
#         'mine': mine,
#         'mine_miner_list': mine_miner_list,
#         'title': 'Maklumat Lombong',
#     }

#     return render(request, 'mine/state/detail.html', context)


# def user_mine_list(request, pk):
#     user = get_object_or_404(User, pk=pk)
#     mine_miner_list = MineMiner.objects.filter(miner=user)

#     page = request.GET.get('page', 1)

#     paginator = Paginator(mine_miner_list, 10)
#     try:
#         mine_miner_list = paginator.page(page)
#     except PageNotAnInteger:
#         mine_miner_list = paginator.page(1)
#     except EmptyPage:
#         mine_miner_list = paginator.page(paginator.num_pages)

#     context = {
#         'each_user': user,
#         'mine_miner_list': mine_miner_list,
#         'title': 'Maklumat Pengguna',
#     }

#     return render(request, 'mine/state/list_user.html', context)


# # def data_detail(request, pk):
# #     data = get_object_or_404(Data, pk=pk)
# #     next_link = reverse('mine:state:statistic',
# #                         kwargs={"pk": data.pk})

# #     context = {
# #         'title': 'Data Lombong',
# #         'data': data,
# #         'next_link': next_link,
# #     }

# #     return render(request, 'mine/state/data/detail.html', context=context)


# def statistic_detail(request, pk):
#     data = get_object_or_404(Data, pk=pk)
#     prev_link = reverse('mine:state:data',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('mine:state:local_worker',
#                         kwargs={"pk": data.pk})
#     statistic = get_list_or_404(MainStatistic, data=data)

#     context = {
#         'title': 'Perangkaan',
#         'statistic': statistic,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'mine/state/data/statistic/detail.html', context=context)


# def local_worker_detail(request, pk):
#     data = get_object_or_404(Data, pk=pk)
#     prev_link = reverse('mine:state:statistic',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('mine:state:foreign_worker',
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

#     return render(request, 'mine/state/data/worker/detail.html', context=context)


# def foreign_worker_detail(request, pk):
#     data = get_object_or_404(Data, pk=pk)
#     prev_link = reverse('mine:state:local_worker',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('mine:state:machinery',
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

#     return render(request, 'mine/state/data/worker/detail.html', context=context)


# def machinery_detail(request, pk):
#     data = get_object_or_404(Data, pk=pk)
#     prev_link = reverse('mine:state:foreign_worker',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('mine:state:energy_supply',
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

#     return render(request, 'mine/state/data/machinery/detail.html', context=context)


# def energy_supply_detail(request, pk):
#     data = get_object_or_404(Data, pk=pk)
#     prev_link = reverse('mine:state:machinery',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('mine:state:operating_record',
#                         kwargs={"pk": data.pk})
#     energy_supply = get_object_or_404(EnergySupply, data=data)

#     context = {
#         'title': 'Bahan Tenaga',
#         'energy_supply': energy_supply,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'mine/state/data/energy_supply/detail.html', context=context)


# def operating_record_detail(request, pk):
#     data = get_object_or_404(Data, pk=pk)
#     prev_link = reverse('mine:state:energy_supply',
#                         kwargs={"pk": data.pk})
#     operating_record = get_object_or_404(
#         OperatingRecord, data=data)

#     if request.method == 'POST':
#         approved = False
#         if request.POST.get('choice') == 'yes':
#             approved = True

#         data_approval = data.get_last_approval()
#         data_approval.state_inspector = request.user
#         data_approval.state_comment = request.POST.get('comment', '')
#         data_approval.state_approved = approved
#         data_approval.save()

#         if approved:
#             jmg_state_admins = User.objects.filter(
#                 groups__name='JMG State Admin', profile__state=data.state)

#             notify = Notify()
#             notify_message = f'{data.miner.mine} telah menghantar permohonan data untuk kuari "{data.mine}"'
#             notify_link = reverse('mine:state_admin:data_list')

#             for jmg_state_admin in jmg_state_admins:
#                 notify.make_notify(
#                     jmg_state_admin, notify_message, notify_link)
#         else:
#             miner = data_approval.requestor

#             notify = Notify()
#             notify_message = f'Data untuk lombong "{data.mine}" telah ditolak'
#             notify_link = reverse('mine:data_list')

#             notify.make_notify(miner, notify_message, notify_link)

#         return redirect('mine:state:data_list')

#     context = {
#         'title': 'Rekod Operasi',
#         'operating_record': operating_record,
#         'prev_link': prev_link,
#         'data_id': data.id,
#     }

#     return render(request, 'mine/state/data/operating_record/detail.html', context=context)
