from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView

from account.models import User
from notification.notify import Notify

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
    MineDataApproval,
)
from ..forms.main import (
    MineMinerDataForm,
    StatisticForm,
    LocalOperatorForm,
    LocalContractorForm,
    ForeignOperatorForm,
    ForeignContractorForm,
    InternalCombustionMachineryForm,
    ElectricMachineryForm,
    EnergySupplyForm,
    OperatingRecordForm,
)


class MineMinerListView(ListView):
    template_name = 'mine/list.html'
    model = MineMiner
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            miner=self.request.user)
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


class MineMinerDataListView(ListView):
    template_name = 'mine/miner_data/list.html'
    model = MineMinerData
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            miner__miner=self.request.user)
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


def add_report(request, pk):
    mine_miner = get_object_or_404(MineMiner, pk=pk)

    if request.method == 'POST':
        form = MineMinerDataForm(request.POST)
        if form.is_valid():
            form.instance.miner = mine_miner
            form.instance.mine = mine_miner.mine
            form.instance.state = mine_miner.mine.state
            miner_data = form.save()

            return redirect('mine:statistic_edit', pk=miner_data.id)

    else:
        form = MineMinerDataForm()

    context = {
        'form': form,
        'title': 'Tambah Data Lombong',
    }

    return render(request, 'mine/miner_data/form.html', context)


def statistic_edit(request, pk):
    miner_data = get_object_or_404(MineMinerData, pk=pk)
    try:
        statistic = Statistic.objects.get(miner_data=miner_data)
    except Statistic.DoesNotExist:
        statistic = None

    if request.method == 'POST':
        if statistic == None:
            form = StatisticForm(request.POST)
        else:
            form = StatisticForm(
                request.POST, instance=statistic)

        if form.is_valid():
            form.instance.miner_data = miner_data
            form.save()
            return redirect('mine:local_worker_edit', pk=miner_data.pk)

    else:
        if statistic == None:
            form = StatisticForm()
        else:
            form = StatisticForm(instance=statistic)

    context = {
        'title': 'Edit Perangkaan',
        'form': form,
    }

    return render(request, 'mine/miner_data/statistic/form.html', context=context)


def local_worker_edit(request, pk):
    miner_data = get_object_or_404(MineMinerData, pk=pk)
    prev_link = reverse('mine:statistic_edit',
                        kwargs={"pk": miner_data.pk})
    try:
        local_operator = LocalOperator.objects.get(miner_data=miner_data)
        local_contractor = LocalContractor.objects.get(miner_data=miner_data)
    except LocalOperator.DoesNotExist:
        local_operator = None
        local_contractor = None

    if request.method == 'POST':
        if local_operator == None:
            operator_form = LocalOperatorForm(request.POST)
            contractor_form = LocalContractorForm(
                request.POST, prefix='second')
        else:
            operator_form = LocalOperatorForm(
                request.POST, instance=local_operator)
            contractor_form = LocalContractorForm(
                request.POST, instance=local_contractor, prefix='second')

        if operator_form.is_valid() and contractor_form.is_valid():
            operator_form.instance.miner_data = miner_data
            contractor_form.instance.miner_data = miner_data
            operator_form.save()
            contractor_form.save()
            return redirect('mine:foreign_worker_edit', pk=miner_data.pk)

    else:
        if local_operator == None:
            operator_form = LocalOperatorForm()
            contractor_form = LocalContractorForm(prefix='second')
        else:
            operator_form = LocalOperatorForm(instance=local_operator)
            contractor_form = LocalContractorForm(
                instance=local_contractor, prefix='second')

    context = {
        'title': 'Edit Pekerjaan (Tempatan)',
        'operator_form': operator_form,
        'contractor_form': contractor_form,
        'prev_link': prev_link,
    }

    return render(request, 'mine/miner_data/worker/form.html', context=context)


def foreign_worker_edit(request, pk):
    miner_data = get_object_or_404(MineMinerData, pk=pk)
    prev_link = reverse('mine:local_worker_edit',
                        kwargs={"pk": miner_data.pk})
    try:
        foreign_operator = ForeignOperator.objects.get(miner_data=miner_data)
        foreign_contractor = ForeignContractor.objects.get(
            miner_data=miner_data)
    except ForeignOperator.DoesNotExist:
        foreign_operator = None
        foreign_contractor = None

    if request.method == 'POST':
        if foreign_operator == None:
            operator_form = ForeignOperatorForm(request.POST)
            contractor_form = ForeignContractorForm(
                request.POST, prefix='second')
        else:
            operator_form = ForeignOperatorForm(
                request.POST, instance=foreign_operator)
            contractor_form = ForeignContractorForm(
                request.POST, instance=foreign_contractor, prefix='second')

        if operator_form.is_valid() and contractor_form.is_valid():
            operator_form.instance.miner_data = miner_data
            contractor_form.instance.miner_data = miner_data
            operator_form.save()
            contractor_form.save()
            return redirect('mine:machinery_edit', pk=miner_data.pk)

    else:
        if foreign_operator == None:
            operator_form = ForeignOperatorForm()
            contractor_form = ForeignContractorForm(prefix='second')
        else:
            operator_form = ForeignOperatorForm(instance=foreign_operator)
            contractor_form = ForeignContractorForm(
                instance=foreign_contractor, prefix='second')

    context = {
        'title': 'Edit Pekerjaan (Asing)',
        'operator_form': operator_form,
        'contractor_form': contractor_form,
        'prev_link': prev_link,
    }

    return render(request, 'mine/miner_data/worker/form.html', context=context)


def machinery_edit(request, pk):
    miner_data = get_object_or_404(MineMinerData, pk=pk)
    prev_link = reverse('mine:foreign_worker_edit',
                        kwargs={"pk": miner_data.pk})
    try:
        combustion_machinery = InternalCombustionMachinery.objects.get(
            miner_data=miner_data)
        electric_machinery = ElectricMachinery.objects.get(
            miner_data=miner_data)
    except InternalCombustionMachinery.DoesNotExist:
        combustion_machinery = None
        electric_machinery = None

    if request.method == 'POST':
        if combustion_machinery == None:
            combustion_form = InternalCombustionMachineryForm(request.POST)
            electric_form = ElectricMachineryForm(
                request.POST, prefix='second')
        else:
            combustion_form = InternalCombustionMachineryForm(
                request.POST, instance=combustion_machinery)
            electric_form = ElectricMachineryForm(
                request.POST, instance=electric_machinery, prefix='second')

        if combustion_form.is_valid() and electric_form.is_valid():
            combustion_form.instance.miner_data = miner_data
            electric_form.instance.miner_data = miner_data
            combustion_form.save()
            electric_form.save()
            return redirect('mine:energy_supply_edit', pk=miner_data.pk)

    else:
        if combustion_machinery == None:
            combustion_form = InternalCombustionMachineryForm()
            electric_form = ElectricMachineryForm(prefix='second')
        else:
            combustion_form = InternalCombustionMachineryForm(
                instance=combustion_machinery)
            electric_form = ElectricMachineryForm(
                instance=electric_machinery, prefix='second')

    context = {
        'title': 'Edit Jentera',
        'combustion_form': combustion_form,
        'electric_form': electric_form,
        'prev_link': prev_link,
    }

    return render(request, 'mine/miner_data/machinery/form.html', context=context)


def energy_supply_edit(request, pk):
    miner_data = get_object_or_404(MineMinerData, pk=pk)
    prev_link = reverse('mine:machinery_edit',
                        kwargs={"pk": miner_data.pk})
    try:
        energy_supply = EnergySupply.objects.get(miner_data=miner_data)
    except EnergySupply.DoesNotExist:
        energy_supply = None

    if request.method == 'POST':
        if energy_supply == None:
            form = EnergySupplyForm(request.POST)
        else:
            form = EnergySupplyForm(
                request.POST, instance=energy_supply)

        if form.is_valid():
            form.instance.miner_data = miner_data
            form.save()
            return redirect('mine:operating_record_edit', pk=miner_data.pk)

    else:
        if energy_supply == None:
            form = EnergySupplyForm()
        else:
            form = EnergySupplyForm(instance=energy_supply)

    context = {
        'title': 'Edit Bahan Tenaga',
        'form': form,
        'prev_link': prev_link,
    }

    return render(request, 'mine/miner_data/energy_supply/form.html', context=context)


def operating_record_edit(request, pk):
    miner_data = get_object_or_404(MineMinerData, pk=pk)
    prev_link = reverse('mine:energy_supply_edit',
                        kwargs={"pk": miner_data.pk})
    try:
        operating_record = OperatingRecord.objects.get(miner_data=miner_data)
    except OperatingRecord.DoesNotExist:
        operating_record = None

    if request.method == 'POST':
        if operating_record == None:
            form = OperatingRecordForm(request.POST)
        else:
            form = OperatingRecordForm(
                request.POST, instance=operating_record)

        if form.is_valid():
            form.instance.miner_data = miner_data
            form.save()
            data_approval = MineDataApproval.objects.create(
                miner_data=miner_data, requestor=request.user)

            jmg_states = User.objects.filter(
                groups__name='JMG State', profile__state=miner_data.state)

            notify = Notify()
            notify_message = f'{request.user} telah menghantar permohonan data untuk lombong "{miner_data.mine}"'
            notify_link = reverse('mine:state:data_list')

            for jmg_state in jmg_states:
                notify.make_notify(jmg_state, notify_message, notify_link)

            return redirect('mine:data_list')

    else:
        if operating_record == None:
            form = OperatingRecordForm()
        else:
            form = OperatingRecordForm(instance=operating_record)

    context = {
        'title': 'Edit Rekod Operasi',
        'form': form,
        'prev_link': prev_link,
    }

    return render(request, 'mine/miner_data/operating_record/form.html', context=context)


def miner_data_delete(request, pk):
    miner_data = get_object_or_404(MineMinerData, pk=pk)

    if miner_data.miner.miner == request.user:
        miner_data.delete()

    return redirect('mine:data_list')


def miner_data_detail(request, pk):
    miner_data = get_object_or_404(MineMinerData, pk=pk)
    next_link = reverse('mine:statistic',
                        kwargs={"pk": miner_data.pk})

    context = {
        'title': 'Data Kuari',
        'miner_data': miner_data,
        'next_link': next_link,
    }

    return render(request, 'mine/miner_data/detail.html', context=context)


def statistic_detail(request, pk):
    miner_data = get_object_or_404(MineMinerData, pk=pk)
    prev_link = reverse('mine:miner_data',
                        kwargs={"pk": miner_data.pk})
    next_link = reverse('mine:local_worker',
                        kwargs={"pk": miner_data.pk})
    statistic = get_object_or_404(Statistic, miner_data=miner_data)

    context = {
        'title': 'Perangkaan',
        'statistic': statistic,
        'prev_link': prev_link,
        'next_link': next_link,
    }

    return render(request, 'mine/miner_data/statistic/detail.html', context=context)


def local_worker_detail(request, pk):
    miner_data = get_object_or_404(MineMinerData, pk=pk)
    prev_link = reverse('mine:statistic',
                        kwargs={"pk": miner_data.pk})
    next_link = reverse('mine:foreign_worker',
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

    return render(request, 'mine/miner_data/worker/detail.html', context=context)


def foreign_worker_detail(request, pk):
    miner_data = get_object_or_404(MineMinerData, pk=pk)
    prev_link = reverse('mine:local_worker',
                        kwargs={"pk": miner_data.pk})
    next_link = reverse('mine:machinery',
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

    return render(request, 'mine/miner_data/worker/detail.html', context=context)


def machinery_detail(request, pk):
    miner_data = get_object_or_404(MineMinerData, pk=pk)
    prev_link = reverse('mine:foreign_worker',
                        kwargs={"pk": miner_data.pk})
    next_link = reverse('mine:energy_supply',
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

    return render(request, 'mine/miner_data/machinery/detail.html', context=context)


def energy_supply_detail(request, pk):
    miner_data = get_object_or_404(MineMinerData, pk=pk)
    prev_link = reverse('mine:machinery',
                        kwargs={"pk": miner_data.pk})
    next_link = reverse('mine:operating_record',
                        kwargs={"pk": miner_data.pk})
    energy_supply = get_object_or_404(EnergySupply, miner_data=miner_data)

    context = {
        'title': 'Bahan Tenaga',
        'energy_supply': energy_supply,
        'prev_link': prev_link,
        'next_link': next_link,
    }

    return render(request, 'mine/miner_data/energy_supply/detail.html', context=context)


def operating_record_detail(request, pk):
    miner_data = get_object_or_404(MineMinerData, pk=pk)
    prev_link = reverse('mine:energy_supply',
                        kwargs={"pk": miner_data.pk})
    operating_record = get_object_or_404(
        OperatingRecord, miner_data=miner_data)

    context = {
        'title': 'Rekod Operasi',
        'operating_record': operating_record,
        'prev_link': prev_link,
        'miner_data_id': miner_data.id,
    }

    return render(request, 'mine/miner_data/operating_record/detail.html', context=context)


def get_comment_data(request, pk):
    data_miner = get_object_or_404(MineMinerData, pk=pk)
    data_approval = data_miner.get_last_approval()
    if data_approval.admin_comment:
        return HttpResponse(data_approval.admin_comment)
    elif data_approval.state_comment:
        return HttpResponse(data_approval.state_comment)
    else:
        return HttpResponse('')
