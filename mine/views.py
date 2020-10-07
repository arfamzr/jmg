from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView

from .models import (
    Mine,
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
from .forms import (
    MineForm,
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


class MineListView(ListView):
    template_name = 'mine/list.html'
    model = Mine
    paginate_by = 10
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Senarai Lombong'
        return context


class MineCreateView(CreateView):
    template_name = 'mine/form.html'
    model = Mine
    form_class = MineForm
    success_url = reverse_lazy('mine:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'RPLB Ringkasan Perangkaan Lombong Bulan'
        return context


class MineUpdateView(UpdateView):
    template_name = 'mine/form.html'
    model = Mine
    form_class = MineForm
    success_url = reverse_lazy('mine:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'RPLB Ringkasan Perangkaan Lombong Bulan (update)'
        return context


def statistic_edit(request, pk):
    mine = get_object_or_404(Mine, pk=pk)
    try:
        statistic = Statistic.objects.get(mine=mine)
    except Statistic.DoesNotExist:
        statistic = None

    if request.method == 'POST':
        if statistic == None:
            form = StatisticForm(request.POST)
        else:
            form = StatisticForm(
                request.POST, instance=statistic)

        if form.is_valid():
            form.instance.mine = mine
            form.save()
            return redirect('mine:local_worker_edit', pk=mine.pk)

    else:
        if statistic == None:
            form = StatisticForm()
        else:
            form = StatisticForm(instance=statistic)

    context = {
        'title': 'Edit Perangkaan',
        'form': form,
    }

    return render(request, 'mine/statistic/form.html', context=context)


def local_worker_edit(request, pk):
    mine = get_object_or_404(Mine, pk=pk)
    prev_link = reverse('mine:statistic_edit',
                        kwargs={"pk": mine.pk})
    try:
        local_operator = LocalOperator.objects.get(mine=mine)
        local_contractor = LocalContractor.objects.get(mine=mine)
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
            operator_form.instance.mine = mine
            contractor_form.instance.mine = mine
            operator_form.save()
            contractor_form.save()
            return redirect('mine:foreign_worker_edit', pk=mine.pk)

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

    return render(request, 'mine/worker/form.html', context=context)


def foreign_worker_edit(request, pk):
    mine = get_object_or_404(Mine, pk=pk)
    prev_link = reverse('mine:local_worker_edit',
                        kwargs={"pk": mine.pk})
    try:
        foreign_operator = ForeignOperator.objects.get(mine=mine)
        foreign_contractor = ForeignContractor.objects.get(mine=mine)
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
            operator_form.instance.mine = mine
            contractor_form.instance.mine = mine
            operator_form.save()
            contractor_form.save()
            return redirect('mine:machinery_edit', pk=mine.pk)

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

    return render(request, 'mine/worker/form.html', context=context)


def machinery_edit(request, pk):
    mine = get_object_or_404(Mine, pk=pk)
    prev_link = reverse('mine:foreign_worker_edit',
                        kwargs={"pk": mine.pk})
    try:
        combustion_machinery = InternalCombustionMachinery.objects.get(
            mine=mine)
        electric_machinery = ElectricMachinery.objects.get(mine=mine)
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
            combustion_form.instance.mine = mine
            electric_form.instance.mine = mine
            combustion_form.save()
            electric_form.save()
            return redirect('mine:energy_supply_edit', pk=mine.pk)

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

    return render(request, 'mine/machinery/form.html', context=context)


def energy_supply_edit(request, pk):
    mine = get_object_or_404(Mine, pk=pk)
    prev_link = reverse('mine:machinery_edit',
                        kwargs={"pk": mine.pk})
    try:
        energy_supply = EnergySupply.objects.get(mine=mine)
    except EnergySupply.DoesNotExist:
        energy_supply = None

    if request.method == 'POST':
        if energy_supply == None:
            form = EnergySupplyForm(request.POST)
        else:
            form = EnergySupplyForm(
                request.POST, instance=energy_supply)

        if form.is_valid():
            form.instance.mine = mine
            form.save()
            return redirect('mine:operating_record_edit', pk=mine.pk)

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

    return render(request, 'mine/energy_supply/form.html', context=context)


def operating_record_edit(request, pk):
    mine = get_object_or_404(Mine, pk=pk)
    prev_link = reverse('mine:energy_supply_edit',
                        kwargs={"pk": mine.pk})
    try:
        operating_record = OperatingRecord.objects.get(mine=mine)
    except OperatingRecord.DoesNotExist:
        operating_record = None

    if request.method == 'POST':
        if operating_record == None:
            form = OperatingRecordForm(request.POST)
        else:
            form = OperatingRecordForm(
                request.POST, instance=operating_record)

        if form.is_valid():
            form.instance.mine = mine
            form.save()
            return redirect('mine:list')

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

    return render(request, 'mine/operating_record/form.html', context=context)
