from django.http import Http404, HttpResponse
from django.http import request
from django.shortcuts import render, get_object_or_404, redirect
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
    SideStatistic,
    LocalOperator,
    LocalContractor,
    ForeignOperator,
    ForeignContractor,
    InternalCombustionMachinery,
    ElectricMachinery,
    EnergySupply,
    OperatingRecord,
    Approval,
)
from ..forms.main import (
    DataForm,
    MainStatisticForm,
    SideStatisticForm,
    LocalOperatorForm,
    LocalContractorForm,
    ForeignOperatorForm,
    ForeignContractorForm,
    InternalCombustionMachineryForm,
    ElectricMachineryForm,
    EnergySupplyForm,
    OperatingRecordForm,
)


# data views
class DataListView(ListView):
    template_name = 'mine/data/list.html'
    model = Data
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            manager__user=self.request.user)
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


class DataCreateView(CreateView):
    model = Data
    form_class = DataForm
    template_name = 'mine/data/form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['manager'] = self.request.user.minemanager
        return kwargs

    def form_valid(self, form):
        form.instance.manager = self.request.user.minemanager
        form.instance.mine = self.request.user.minemanager.mine
        form.instance.state = self.request.user.minemanager.mine.state
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mine:statistic_edit', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Tambah RPLB'
        return context


def data_delete(request, pk):
    if request.method == 'POST':
        data = get_object_or_404(Data, pk=pk)

        if data.manager.user == request.user:
            data.delete()

    return redirect('mine:data_list')


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

    context = {
        'title': 'Data Lombong',
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

    return render(request, 'mine/data/detail.html', context=context)


# statistic views
def statistic_edit(request, pk):
    data = get_object_or_404(Data, pk=pk)
    main_statistic_list = MainStatistic.objects.filter(data=data)
    side_statistic_list = SideStatistic.objects.filter(data=data)
    next_link = reverse('mine:local_worker_edit', kwargs={'pk': data.pk})

    context = {
        'title': 'Perangkaan',
        'data': data,
        'main_statistic_list': main_statistic_list,
        'side_statistic_list': side_statistic_list,
        'next_link': next_link,
    }

    return render(request, 'mine/data/statistic/list.html', context)


class MainStatisticCreateView(CreateView):
    template_name = 'mine/data/statistic/form.html'
    form_class = MainStatisticForm
    model = MainStatistic

    def form_valid(self, form):
        self.data = get_object_or_404(
            Data, pk=self.kwargs['pk'])
        form.instance.data = self.data
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mine:statistic_edit', kwargs={'pk': self.data.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Tambah Perangkaan Mineral Utama'
        return context


class MainStatisticUpdateView(UpdateView):
    template_name = 'mine/data/statistic/form.html'
    form_class = MainStatisticForm
    model = MainStatistic

    def get_success_url(self):
        return reverse('mine:statistic_edit', kwargs={'pk': self.object.data.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Perangkaan Mineral Utama'
        return context


def main_statistic_delete(request, pk):
    main_statistic = get_object_or_404(MainStatistic, pk=pk)
    if request.method == 'POST':
        main_statistic.delete()
    return redirect('mine:statistic_edit', pk=main_statistic.data.pk)


def main_statistic_detail(request, pk):
    main_statistic = get_object_or_404(MainStatistic, pk=pk)
    next_link = reverse("mine:data_detail", kwargs={
                        "pk": main_statistic.data.pk})

    context = {
        'title': 'Perangkaan Mineral Utama',
        'next_link': next_link,
        'statistic': main_statistic,
    }

    return render(request, 'mine/data/statistic/detail.html', context)


class SideStatisticCreateView(CreateView):
    template_name = 'mine/data/statistic/form.html'
    form_class = SideStatisticForm
    model = SideStatistic

    def form_valid(self, form):
        self.data = get_object_or_404(
            Data, pk=self.kwargs['pk'])
        form.instance.data = self.data
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mine:statistic_edit', kwargs={'pk': self.data.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Tambah Perangkaan Mineral Sampingan'
        return context


class SideStatisticUpdateView(UpdateView):
    template_name = 'mine/data/statistic/form.html'
    form_class = SideStatisticForm
    model = SideStatistic

    def get_success_url(self):
        return reverse('mine:statistic_edit', kwargs={'pk': self.object.data.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Perangkaan Mineral Sampingan'
        return context


def side_statistic_delete(request, pk):
    side_statistic = get_object_or_404(SideStatistic, pk=pk)
    if request.method == 'POST':
        side_statistic.delete()
    return redirect('mine:statistic_edit', pk=side_statistic.data.pk)


def side_statistic_detail(request, pk):
    side_statistic = get_object_or_404(SideStatistic, pk=pk)
    next_link = reverse("mine:data_detail", kwargs={
                        "pk": side_statistic.data.pk})

    context = {
        'title': 'Perangkaan Mineral Sampingan',
        'next_link': next_link,
        'statistic': side_statistic,
    }

    return render(request, 'mine/data/statistic/detail.html', context)


# local worker views
def local_worker_edit(request, pk):
    data = get_object_or_404(Data, pk=pk)
    prev_link = reverse('mine:statistic_edit',
                        kwargs={"pk": data.pk})
    try:
        local_operator = LocalOperator.objects.get(data=data)
        local_contractor = LocalContractor.objects.get(data=data)
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
            operator_form.instance.data = data
            contractor_form.instance.data = data
            operator_form.save()
            contractor_form.save()
            return redirect('mine:foreign_worker_edit', pk=data.pk)
        else:
            print(operator_form.errors)
            print(contractor_form.errors)

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

    return render(request, 'mine/data/worker/form.html', context=context)


# foreign worker views
def foreign_worker_edit(request, pk):
    data = get_object_or_404(Data, pk=pk)
    prev_link = reverse('mine:local_worker_edit',
                        kwargs={"pk": data.pk})
    try:
        foreign_operator = ForeignOperator.objects.get(data=data)
        foreign_contractor = ForeignContractor.objects.get(
            data=data)
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
            operator_form.instance.data = data
            contractor_form.instance.data = data
            operator_form.save()
            contractor_form.save()
            return redirect('mine:machinery_edit', pk=data.pk)

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

    return render(request, 'mine/data/worker/form.html', context=context)


# machinery views
def machinery_edit(request, pk):
    data = get_object_or_404(Data, pk=pk)
    prev_link = reverse('mine:foreign_worker_edit',
                        kwargs={"pk": data.pk})
    try:
        combustion_machinery = InternalCombustionMachinery.objects.get(
            data=data)
        electric_machinery = ElectricMachinery.objects.get(
            data=data)
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
            combustion_form.instance.data = data
            electric_form.instance.data = data
            combustion_form.save()
            electric_form.save()
            return redirect('mine:energy_supply_edit', pk=data.pk)

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

    return render(request, 'mine/data/machinery/form.html', context=context)


# energy supply views
def energy_supply_edit(request, pk):
    data = get_object_or_404(Data, pk=pk)
    prev_link = reverse('mine:machinery_edit',
                        kwargs={"pk": data.pk})
    try:
        energy_supply = EnergySupply.objects.get(data=data)
    except EnergySupply.DoesNotExist:
        energy_supply = None

    if request.method == 'POST':
        if energy_supply == None:
            form = EnergySupplyForm(request.POST)
        else:
            form = EnergySupplyForm(
                request.POST, instance=energy_supply)

        if form.is_valid():
            form.instance.data = data
            form.save()
            return redirect('mine:operating_record_edit', pk=data.pk)

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

    return render(request, 'mine/data/energy_supply/form.html', context=context)


# operating record views
def operating_record_edit(request, pk):
    data = get_object_or_404(Data, pk=pk)
    prev_link = reverse('mine:energy_supply_edit',
                        kwargs={"pk": data.pk})
    try:
        operating_record = OperatingRecord.objects.get(data=data)
    except OperatingRecord.DoesNotExist:
        operating_record = None

    if request.method == 'POST':
        if operating_record == None:
            form = OperatingRecordForm(request.POST)
        else:
            form = OperatingRecordForm(
                request.POST, instance=operating_record)

        if form.is_valid():
            form.instance.data = data
            form.save()

            return redirect('mine:data_summary', data.pk)

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

    return render(request, 'mine/data/operating_record/form.html', context=context)

# summary views


def data_summary(request, pk):
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

    prev_link = reverse('mine:operating_record_edit',
                        kwargs={"pk": data.pk})

    if request.method == 'POST':
        data_approval = Approval.objects.create(
            data=data, requestor=request.user)

        jmg_states = User.objects.filter(
            groups__name='JMG State', profile__state=data.state)

        notify = Notify()
        notify_message = f'{request.user} telah menghantar permohonan data untuk lombong "{data.mine}"'
        notify_link = reverse('mine:state:data_list')

        for jmg_state in jmg_states:
            notify.make_notify(jmg_state, notify_message, notify_link)

        return redirect('mine:data_list')

    context = {
        'title': 'Data Lombong',
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

    return render(request, 'mine/data/summary.html', context)

# comment views


def get_comment_data(request, pk):
    data = get_object_or_404(Data, pk=pk)
    data_approval = data.get_last_approval()
    if data_approval.admin_comment:
        return HttpResponse(data_approval.admin_comment)
    elif data_approval.state_comment:
        return HttpResponse(data_approval.state_comment)
    else:
        return HttpResponse('')


# summary views
def data_summary(request, pk):
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

    prev_link = reverse('mine:operating_record_edit',
                        kwargs={"pk": data.pk})

    if request.method == 'POST':
        data_approval = Approval.objects.create(
            data=data, requestor=request.user)

        jmg_states = User.objects.filter(
            groups__name='JMG State', profile__state=data.state)

        notify = Notify()
        notify_message = f'{request.user} telah menghantar permohonan data untuk lombong "{data.mine}"'
        notify_link = reverse('mine:state:data_list')

        for jmg_state in jmg_states:
            notify.make_notify(jmg_state, notify_message, notify_link)

        return redirect('mine:data_list')

    context = {
        'title': 'Data Lombong',
        'data': data,
        'local_operator': local_operator,
        'local_contractor': local_contractor,
        'foreign_operator': foreign_operator,
        'foreign_contractor': foreign_contractor,
        'combustion_machinery': combustion_machinery,
        'electric_machinery': electric_machinery,
        'energy_supply': energy_supply,
        'operating_record': operating_record,
        'prev_link': prev_link,
    }

    return render(request, 'mine/data/summary.html', context=context)


# class MineMinerListView(ListView):
#     template_name = 'mine/list.html'
#     model = MineMiner
#     paginate_by = 10
#     ordering = ['-created_at']

#     def get_queryset(self):
#         queryset = super().get_queryset().filter(
#             miner=self.request.user)
#         try:
#             name = self.request.GET['q']
#         except:
#             name = ''
#         if (name != ''):
#             object_list = queryset.filter(location__icontains=name)
#         else:
#             object_list = queryset
#         return object_list

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = 'Senarai Lombong'
#         return context


# def add_report(request, pk):
#     mine_miner = get_object_or_404(MineMiner, pk=pk)

#     if request.method == 'POST':
#         form = DataForm(request.POST)
#         if form.is_valid():
#             form.instance.miner = mine_miner
#             form.instance.mine = mine_miner.mine
#             form.instance.state = mine_miner.mine.state
#             data = form.save()

#             return redirect('mine:statistic_edit', pk=data.id)

#     else:
#         form = DataForm()

#     context = {
#         'form': form,
#         'title': 'Tambah Data Lombong',
#     }

#     return render(request, 'mine/data/form.html', context)


# # def main_statistic_edit(request, pk):
# #     data = get_object_or_404(Data, pk=pk)
# #     try:
# #         statistic = MainStatistic.objects.get(data=data)
# #     except MainStatistic.DoesNotExist:
# #         statistic = None

# #     if request.method == 'POST':
# #         if statistic == None:
# #             form = MainStatisticForm(request.POST)
# #         else:
# #             form = MainStatisticForm(
# #                 request.POST, instance=statistic)

# #         if form.is_valid():
# #             form.instance.data = data
# #             form.save()
# #             return redirect('mine:local_worker_edit', pk=data.pk)

# #     else:
# #         if statistic == None:
# #             form = MainStatisticForm()
# #         else:
# #             form = MainStatisticForm(instance=statistic)

# #     context = {
# #         'title': 'Perangkaan Mineral Utama',
# #         'form': form,
# #     }

# #     return render(request, 'mine/data/statistic/form.html', context=context)


# # def data_detail(request, pk):
# #     data = get_object_or_404(Data, pk=pk)
# #     next_link = reverse('mine:statistic',
# #                         kwargs={"pk": data.pk})

# #     context = {
# #         'title': 'Data Kuari',
# #         'data': data,
# #         'next_link': next_link,
# #     }

# #     return render(request, 'mine/data/detail.html', context=context)


# def statistic_detail(request, pk):
#     data = get_object_or_404(Data, pk=pk)
#     prev_link = reverse('mine:data',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('mine:local_worker',
#                         kwargs={"pk": data.pk})
#     statistic = get_object_or_404(MainStatistic, data=data)

#     context = {
#         'title': 'Perangkaan',
#         'statistic': statistic,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'mine/data/statistic/detail.html', context=context)


# def local_worker_detail(request, pk):
#     data = get_object_or_404(Data, pk=pk)
#     prev_link = reverse('mine:statistic',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('mine:foreign_worker',
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

#     return render(request, 'mine/data/worker/detail.html', context=context)


# def foreign_worker_detail(request, pk):
#     data = get_object_or_404(Data, pk=pk)
#     prev_link = reverse('mine:local_worker',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('mine:machinery',
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

#     return render(request, 'mine/data/worker/detail.html', context=context)


# def machinery_detail(request, pk):
#     data = get_object_or_404(Data, pk=pk)
#     prev_link = reverse('mine:foreign_worker',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('mine:energy_supply',
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

#     return render(request, 'mine/data/machinery/detail.html', context=context)


# def energy_supply_detail(request, pk):
#     data = get_object_or_404(Data, pk=pk)
#     prev_link = reverse('mine:machinery',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('mine:operating_record',
#                         kwargs={"pk": data.pk})
#     energy_supply = get_object_or_404(EnergySupply, data=data)

#     context = {
#         'title': 'Bahan Tenaga',
#         'energy_supply': energy_supply,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'mine/data/energy_supply/detail.html', context=context)


# def operating_record_detail(request, pk):
#     data = get_object_or_404(Data, pk=pk)
#     prev_link = reverse('mine:energy_supply',
#                         kwargs={"pk": data.pk})
#     operating_record = get_object_or_404(
#         OperatingRecord, data=data)

#     context = {
#         'title': 'Rekod Operasi',
#         'operating_record': operating_record,
#         'prev_link': prev_link,
#         'data_id': data.id,
#     }

#     return render(request, 'mine/data/operating_record/detail.html', context=context)
