from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView

from account.models import User

from ..models import (
    Mine,
    MineMiner,
    MineMinerData,
    Statistic,
    LocalOperator,
    LocalContractor,
    ForeignOperator,
    ForeignContractor,
    InternalCombustionMachinery,
    ElectricMachinery,
    EnergySupply,
    OperatingRecord,
)


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

    context = {
        'mine': mine,
        'mine_miner_list': mine_miner_list,
        'title': 'Maklumat Lombong',
    }

    return render(request, 'mine/state/detail.html', context)


def user_mine_list(request, pk):
    user = get_object_or_404(User, pk=pk)
    mine_miner_list = MineMiner.objects.filter(miner=user)

    context = {
        'each_user': user,
        'mine_miner_list': mine_miner_list,
        'title': 'Maklumat Pengguna',
    }

    return render(request, 'mine/state/list_user.html', context)


class QuarryMinerDataListView(ListView):
    template_name = 'quarry/state/miner_data/list.html'
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
        context["title"] = 'Senarai Data Lombong'
        return context


def miner_data_detail(request, pk):
    miner_data = get_object_or_404(MineMinerData, pk=pk)
    next_link = reverse('mine:state:statistic',
                        kwargs={"pk": miner_data.pk})

    context = {
        'title': 'Data Kuari',
        'miner_data': miner_data,
        'next_link': next_link,
    }

    return render(request, 'mine/state/miner_data/detail.html', context=context)


def statistic_detail(request, pk):
    miner_data = get_object_or_404(MineMinerData, pk=pk)
    prev_link = reverse('mine:state:miner_data',
                        kwargs={"pk": miner_data.pk})
    next_link = reverse('mine:state:local_worker',
                        kwargs={"pk": miner_data.pk})
    statistic = get_object_or_404(Statistic, miner_data=miner_data)

    context = {
        'title': 'Perangkaan',
        'statistic': statistic,
        'prev_link': prev_link,
        'next_link': next_link,
    }

    return render(request, 'mine/state/miner_data/statistic/detail.html', context=context)


def local_worker_detail(request, pk):
    miner_data = get_object_or_404(MineMinerData, pk=pk)
    prev_link = reverse('mine:state:statistic',
                        kwargs={"pk": miner_data.pk})
    next_link = reverse('mine:state:foreign_worker',
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

    return render(request, 'mine/state/miner_data/worker/detail.html', context=context)


def foreign_worker_detail(request, pk):
    miner_data = get_object_or_404(MineMinerData, pk=pk)
    prev_link = reverse('mine:state:local_worker',
                        kwargs={"pk": miner_data.pk})
    next_link = reverse('mine:state:machinery',
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

    return render(request, 'mine/state/miner_data/worker/detail.html', context=context)


def machinery_detail(request, pk):
    miner_data = get_object_or_404(MineMinerData, pk=pk)
    prev_link = reverse('mine:state:foreign_worker',
                        kwargs={"pk": miner_data.pk})
    next_link = reverse('mine:state:energy_supply',
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

    return render(request, 'mine/state/miner_data/machinery/detail.html', context=context)


def energy_supply_detail(request, pk):
    miner_data = get_object_or_404(MineMinerData, pk=pk)
    prev_link = reverse('mine:state:machinery',
                        kwargs={"pk": miner_data.pk})
    next_link = reverse('mine:state:operating_record',
                        kwargs={"pk": miner_data.pk})
    energy_supply = get_object_or_404(EnergySupply, miner_data=miner_data)

    context = {
        'title': 'Bahan Tenaga',
        'energy_supply': energy_supply,
        'prev_link': prev_link,
        'next_link': next_link,
    }

    return render(request, 'mine/state/miner_data/energy_supply/detail.html', context=context)


def operating_record_detail(request, pk):
    miner_data = get_object_or_404(MineMinerData, pk=pk)
    prev_link = reverse('mine:state:energy_supply',
                        kwargs={"pk": miner_data.pk})
    operating_record = get_object_or_404(
        OperatingRecord, miner_data=miner_data)

    if request.method == 'POST':
        approved = False
        if request.POST.get('choice') == 'yes':
            approved = True

        data_approval = miner_data.get_last_approval()
        data_approval.state_inspector = request.user
        data_approval.state_comment = request.POST.get('comment', '')
        data_approval.state_approved = approved
        data_approval.save()
        return redirect('mine:state:data_list')

    context = {
        'title': 'Rekod Operasi',
        'operating_record': operating_record,
        'prev_link': prev_link,
        'miner_data_id': miner_data.id,
    }

    return render(request, 'mine/state/miner_data/operating_record/detail.html', context=context)
