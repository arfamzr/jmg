from django.db.models import manager
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView

from account.models import User
from notification.notify import Notify

from ..models import (
    Quarry,
    Data,
    MainProductionStatistic,
    SideProductionStatistic,
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
from ..forms.main import (
    DataForm,
    MainProductionStatisticForm,
    SideProductionStatisticForm,
    SalesSubmissionForm,
    LocalFinalUsesForm,
    ExportFinalUsesForm,
    LocalOperatorForm,
    LocalContractorForm,
    ForeignOperatorForm,
    ForeignContractorForm,
    InternalCombustionMachineryForm,
    ElectricMachineryForm,
    DailyExplosiveForm,
    EnergySupplyForm,
    OperatingRecordForm,
    RoyaltiesForm,
    OtherForm,
)


# data views
class DataListView(ListView):
    template_name = 'quarry/data/list.html'
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
        context["title"] = 'Senarai PKB'
        return context


class DataCreateView(CreateView):
    model = Data
    form_class = DataForm
    template_name = 'quarry/data/form.html'

    def form_valid(self, form):
        form.instance.manager = self.request.user.quarrymanager
        form.instance.quarry = self.request.user.quarrymanager.quarry
        form.instance.state = self.request.user.quarrymanager.quarry.state
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('quarry:production_statistic_edit', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Tambah PKB'
        return context


def data_delete(request, pk):
    data = get_object_or_404(Data, pk=pk)

    if data.manager.user == request.user:
        data.delete()

    return redirect('quarry:data_list')


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

    return render(request, 'quarry/data/detail.html', context)


# production statistic views
def production_statistic_edit(request, pk):
    data = get_object_or_404(Data, pk=pk)
    main_statistic_list = MainProductionStatistic.objects.filter(data=data)
    side_statistic_list = SideProductionStatistic.objects.filter(data=data)
    next_link = reverse('quarry:sales_submission_edit', kwargs={'pk': data.pk})

    context = {
        'title': 'Perangkaan Pengeluaran',
        'data': data,
        'main_statistic_list': main_statistic_list,
        'side_statistic_list': side_statistic_list,
        'next_link': next_link,
    }

    return render(request, 'quarry/data/production_statistic/list.html', context=context)


class MainProductionStatisticCreateView(CreateView):
    template_name = 'quarry/data/production_statistic/form.html'
    form_class = MainProductionStatisticForm
    model = MainProductionStatistic

    def form_valid(self, form):
        self.data = get_object_or_404(
            Data, pk=self.kwargs['pk'])
        form.instance.data = self.data
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('quarry:production_statistic_edit', kwargs={'pk': self.data.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Tambah Perangkaan Batuan Utama (Tan Metrik)'
        return context


class MainProductionStatisticUpdateView(UpdateView):
    template_name = 'quarry/data/production_statistic/form.html'
    form_class = MainProductionStatisticForm
    model = MainProductionStatistic

    def get_success_url(self):
        return reverse('quarry:production_statistic_edit', kwargs={'pk': self.object.data.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Perangkaan Batuan Utama (Tan Metrik)'
        return context


def main_production_statistic_delete(request, pk):
    main_statistic = get_object_or_404(MainProductionStatistic, pk=pk)
    main_statistic.delete()
    return redirect('quarry:production_statistic_edit', pk=main_statistic.data.pk)


def main_production_statistic_detail(request, pk):
    main_statistic = get_object_or_404(MainProductionStatistic, pk=pk)
    next_link = reverse("quarry:data_detail", kwargs={
                        "pk": main_statistic.data.pk})

    context = {
        'title': 'Perangkaan Batuan Utama',
        'next_link': next_link,
        'statistic': main_statistic,
    }

    return render(request, 'quarry/data/production_statistic/detail.html', context)


class SideProductionStatisticCreateView(CreateView):
    template_name = 'quarry/data/production_statistic/form.html'
    form_class = SideProductionStatisticForm
    model = SideProductionStatistic

    def form_valid(self, form):
        self.data = get_object_or_404(
            Data, pk=self.kwargs['pk'])
        form.instance.data = self.data
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('quarry:production_statistic_edit', kwargs={'pk': self.data.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Tambah Perangkaan Batuan Sampingan (Tan Metrik)'
        return context


class SideProductionStatisticUpdateView(UpdateView):
    template_name = 'quarry/data/production_statistic/form.html'
    form_class = SideProductionStatisticForm
    model = SideProductionStatistic

    def get_success_url(self):
        return reverse('quarry:production_statistic_edit', kwargs={'pk': self.object.data.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Perangkaan Batuan Sampingan (Tan Metrik)'
        return context


def side_production_statistic_delete(request, pk):
    side_statistic = get_object_or_404(SideProductionStatistic, pk=pk)
    side_statistic.delete()
    return redirect('quarry:production_statistic_edit', pk=side_statistic.data.pk)


def side_production_statistic_detail(request, pk):
    side_statistic = get_object_or_404(SideProductionStatistic, pk=pk)
    next_link = reverse("quarry:data_detail", kwargs={
                        "pk": side_statistic.data.pk})

    context = {
        'title': 'Perangkaan Batuan Sampingan',
        'next_link': next_link,
        'statistic': side_statistic,
    }

    return render(request, 'quarry/data/production_statistic/detail.html', context)


# sales submission views
def sales_submission_edit(request, pk):
    data = get_object_or_404(Data, pk=pk)
    sales_submission_list = SalesSubmission.objects.filter(data=data)
    next_link = reverse('quarry:final_uses_edit', kwargs={'pk': data.pk})

    context = {
        'title': 'Penyerahan Jualan',
        'data': data,
        'sales_submission_list': sales_submission_list,
        'next_link': next_link,
    }

    return render(request, 'quarry/data/sales_submission/list.html', context=context)


class SalesSubmissionCreateView(CreateView):
    template_name = 'quarry/data/sales_submission/form.html'
    form_class = SalesSubmissionForm
    model = SalesSubmission

    def form_valid(self, form):
        self.data = get_object_or_404(
            Data, pk=self.kwargs['pk'])
        form.instance.data = self.data
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('quarry:sales_submission_edit', kwargs={'pk': self.data.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Tambah Penyerahan Jualan'
        return context


class SalesSubmissionUpdateView(UpdateView):
    template_name = 'quarry/data/sales_submission/form.html'
    form_class = SalesSubmissionForm
    model = SalesSubmission

    def get_success_url(self):
        return reverse('quarry:sales_submission_edit', kwargs={'pk': self.object.data.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Penyerahan Jualan'
        return context


def sales_submission_delete(request, pk):
    sales_submission = get_object_or_404(SalesSubmission, pk=pk)
    sales_submission.delete()
    return redirect('quarry:sales_submission_edit', pk=sales_submission.data.pk)


def sales_submission_detail(request, pk):
    sales_submission = get_object_or_404(SalesSubmission, pk=pk)
    next_link = reverse("quarry:data_detail", kwargs={
                        "pk": sales_submission.data.pk})

    context = {
        'title': 'Penyerahan Jualan',
        'next_link': next_link,
        'sales_submission': sales_submission,
    }

    return render(request, 'quarry/data/sales_submission/detail.html', context)


# final uses views
def final_uses_edit(request, pk):
    data = get_object_or_404(Data, pk=pk)
    prev_link = reverse('quarry:sales_submission_edit',
                        kwargs={"pk": data.pk})
    try:
        local_final_uses = LocalFinalUses.objects.get(data=data)
        export_final_uses = ExportFinalUses.objects.get(data=data)
    except LocalFinalUses.DoesNotExist:
        local_final_uses = None
        export_final_uses = None

    if request.method == 'POST':
        if local_final_uses == None:
            local_form = LocalFinalUsesForm(request.POST)
            export_form = ExportFinalUsesForm(request.POST, prefix='second')
        else:
            local_form = LocalFinalUsesForm(
                request.POST, instance=local_final_uses)
            export_form = ExportFinalUsesForm(
                request.POST, instance=export_final_uses, prefix='second')

        if local_form.is_valid() and export_form.is_valid():
            local_form.instance.data = data
            export_form.instance.data = data
            local_form.save()
            export_form.save()
            return redirect('quarry:local_worker_edit', pk=data.pk)

    else:
        if local_final_uses == None:
            local_form = LocalFinalUsesForm()
            export_form = ExportFinalUsesForm(prefix='second')
        else:
            local_form = LocalFinalUsesForm(instance=local_final_uses)
            export_form = ExportFinalUsesForm(
                instance=export_final_uses, prefix='second')

    context = {
        'title': 'Edit Kegunaan Akhir',
        'local_form': local_form,
        'export_form': export_form,
        'prev_link': prev_link,
    }

    return render(request, 'quarry/data/final_uses/form.html', context=context)


# local worker views
def local_worker_edit(request, pk):
    data = get_object_or_404(Data, pk=pk)
    prev_link = reverse('quarry:final_uses_edit',
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
            return redirect('quarry:foreign_worker_edit', pk=data.pk)

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

    return render(request, 'quarry/data/worker/form.html', context=context)


# foreign worker views
def foreign_worker_edit(request, pk):
    data = get_object_or_404(Data, pk=pk)
    prev_link = reverse('quarry:local_worker_edit',
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
            return redirect('quarry:machinery_edit', pk=data.pk)

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

    return render(request, 'quarry/data/worker/form.html', context=context)


# machinery views
def machinery_edit(request, pk):
    data = get_object_or_404(Data, pk=pk)
    prev_link = reverse('quarry:foreign_worker_edit',
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
            return redirect('quarry:daily_explosive_edit', pk=data.pk)

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

    return render(request, 'quarry/data/machinery/form.html', context=context)


# daily explosive views
def daily_explosive_edit(request, pk):
    data = get_object_or_404(Data, pk=pk)
    prev_link = reverse('quarry:machinery_edit',
                        kwargs={"pk": data.pk})
    try:
        daily_explosive = DailyExplosive.objects.get(data=data)
    except DailyExplosive.DoesNotExist:
        daily_explosive = None

    if request.method == 'POST':
        if daily_explosive == None:
            form = DailyExplosiveForm(request.POST)
        else:
            form = DailyExplosiveForm(
                request.POST, instance=daily_explosive)

        if form.is_valid():
            form.instance.data = data
            form.save()
            return redirect('quarry:energy_supply_edit', pk=data.pk)

    else:
        if daily_explosive == None:
            form = DailyExplosiveForm()
        else:
            form = DailyExplosiveForm(instance=daily_explosive)

    context = {
        'title': 'Edit Bahan Letupan Harian',
        'form': form,
        'prev_link': prev_link,
    }

    return render(request, 'quarry/data/daily_explosive/form.html', context=context)


# energy supply views
def energy_supply_edit(request, pk):
    data = get_object_or_404(Data, pk=pk)
    prev_link = reverse('quarry:daily_explosive_edit',
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
            return redirect('quarry:operating_record_edit', pk=data.pk)

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

    return render(request, 'quarry/data/energy_supply/form.html', context=context)


# operating record views
def operating_record_edit(request, pk):
    data = get_object_or_404(Data, pk=pk)
    prev_link = reverse('quarry:energy_supply_edit',
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
            return redirect('quarry:royalties_edit', pk=data.pk)

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

    return render(request, 'quarry/data/operating_record/form.html', context=context)


# royalties views
def royalties_edit(request, pk):
    data = get_object_or_404(Data, pk=pk)
    prev_link = reverse('quarry:operating_record_edit',
                        kwargs={"pk": data.pk})
    try:
        royalties = Royalties.objects.get(data=data)
    except Royalties.DoesNotExist:
        royalties = None

    if request.method == 'POST':
        if royalties == None:
            form = RoyaltiesForm(request.POST)
        else:
            form = RoyaltiesForm(
                request.POST, instance=royalties)

        if form.is_valid():
            form.instance.data = data
            form.save()
            return redirect('quarry:other_edit', pk=data.pk)

    else:
        if royalties == None:
            form = RoyaltiesForm()
        else:
            form = RoyaltiesForm(instance=royalties)

    context = {
        'title': 'Edit Royalti',
        'form': form,
        'prev_link': prev_link,
    }

    return render(request, 'quarry/data/royalties/form.html', context=context)


# other views
def other_edit(request, pk):
    data = get_object_or_404(Data, pk=pk)
    prev_link = reverse('quarry:royalties_edit',
                        kwargs={"pk": data.pk})
    try:
        other = Other.objects.get(data=data)
    except Other.DoesNotExist:
        other = None

    if request.method == 'POST':
        if other == None:
            form = OtherForm(request.POST)
        else:
            form = OtherForm(
                request.POST, instance=other)

        if form.is_valid():
            form.instance.data = data
            form.save()
            data_approval = Approval.objects.create(
                data=data, requestor=request.user)

            # jmg_states = User.objects.filter(
            #     groups__name='JMG State', profile__state=data.state)

            # notify = Notify()
            # notify_message = f'{request.user} telah menghantar permohonan data untuk kuari "{data.quarry}"'
            # notify_link = reverse('quarry:state:data_list')

            # for jmg_state in jmg_states:
            #     notify.make_notify(jmg_state, notify_message, notify_link)

            return redirect('quarry:data_list')

    else:
        if other == None:
            form = OtherForm()
        else:
            form = OtherForm(instance=other)

    context = {
        'title': 'Edit Lain-lain',
        'form': form,
        'prev_link': prev_link,
    }

    return render(request, 'quarry/data/other/form.html', context=context)


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


# class QuarryMinerListView(ListView):
#     template_name = 'quarry/list.html'
#     model = QuarryMiner
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
#         context["title"] = 'Senarai Kuari'
#         return context


# def add_report(request, pk):
#     quarry_miner = get_object_or_404(QuarryMiner, pk=pk)

#     if request.method == 'POST':
#         form = DataForm(request.POST)
#         if form.is_valid():
#             form.instance.miner = quarry_miner
#             form.instance.quarry = quarry_miner.quarry
#             form.instance.state = quarry_miner.quarry.state
#             data = form.save()

#             return redirect('quarry:production_statistic_edit', pk=data.id)

#     else:
#         form = DataForm()

#     context = {
#         'form': form,
#         'title': 'Tambah Data Kuari',
#     }

#     return render(request, 'quarry/data/form.html', context)


# def production_statistic_edit(request, pk):
#     data = get_object_or_404(Data, pk=pk)
#     try:
#         production_statistic = ProductionStatistic.objects.get(
#             data=data)
#     except ProductionStatistic.DoesNotExist:
#         production_statistic = None

#     if request.method == 'POST':
#         if production_statistic == None:
#             form = ProductionStatisticForm(request.POST)
#         else:
#             form = ProductionStatisticForm(
#                 request.POST, instance=production_statistic)

#         if form.is_valid():
#             form.instance.data = data
#             form.save()
#             return redirect('quarry:sales_submission_edit', pk=data.pk)

#     else:
#         if production_statistic == None:
#             form = ProductionStatisticForm()
#         else:
#             form = ProductionStatisticForm(instance=production_statistic)

#     context = {
#         'title': 'Edit Perangkaan Pengeluaran',
#         'form': form,
#     }

#     return render(request, 'quarry/data/production_statistic/form.html', context=context)


# def sales_submission_edit(request, pk):
#     data = get_object_or_404(Data, pk=pk)
#     prev_link = reverse('quarry:production_statistic_edit',
#                         kwargs={"pk": data.pk})
#     try:
#         sales_submission = SalesSubmission.objects.get(data=data)
#     except SalesSubmission.DoesNotExist:
#         sales_submission = None

#     if request.method == 'POST':
#         if sales_submission == None:
#             form = SalesSubmissionForm(request.POST)
#         else:
#             form = SalesSubmissionForm(
#                 request.POST, instance=sales_submission)

#         if form.is_valid():
#             form.instance.data = data
#             form.save()
#             return redirect('quarry:final_uses_edit', pk=data.pk)

#     else:
#         if sales_submission == None:
#             form = SalesSubmissionForm()
#         else:
#             form = SalesSubmissionForm(instance=sales_submission)

#     context = {
#         'title': 'Edit Penyerahan Jualan',
#         'form': form,
#         'prev_link': prev_link,
#     }

#     return render(request, 'quarry/data/sales_submission/form.html', context=context)


# # def data_detail(request, pk):
# #     data = get_object_or_404(Data, pk=pk)
# #     next_link = reverse('quarry:production_statistic',
# #                         kwargs={"pk": data.pk})

# #     context = {
# #         'title': 'Data Kuari',
# #         'data': data,
# #         'next_link': next_link,
# #     }

# #     return render(request, 'quarry/data/detail.html', context=context)


# def production_statistic_detail(request, pk):
#     data = get_object_or_404(Data, pk=pk)
#     prev_link = reverse('quarry:data',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('quarry:sales_submission',
#                         kwargs={"pk": data.pk})
#     production_statistic = get_object_or_404(
#         ProductionStatistic, data=data)

#     context = {
#         'title': 'Perangkaan Pengeluaran',
#         'production_statistic': production_statistic,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/data/production_statistic/detail.html', context=context)


# def sales_submission_detail(request, pk):
#     data = get_object_or_404(Data, pk=pk)
#     prev_link = reverse('quarry:production_statistic',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('quarry:final_uses',
#                         kwargs={"pk": data.pk})
#     sales_submission = get_object_or_404(
#         SalesSubmission, data=data)

#     context = {
#         'title': 'Penyerahan Jualan',
#         'sales_submission': sales_submission,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/data/sales_submission/detail.html', context=context)


# def final_uses_detail(request, pk):
#     data = get_object_or_404(Data, pk=pk)
#     prev_link = reverse('quarry:sales_submission',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('quarry:local_worker',
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

#     return render(request, 'quarry/data/final_uses/detail.html', context=context)


# def local_worker_detail(request, pk):
#     data = get_object_or_404(Data, pk=pk)
#     prev_link = reverse('quarry:final_uses',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('quarry:foreign_worker',
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

#     return render(request, 'quarry/data/worker/detail.html', context=context)


# def foreign_worker_detail(request, pk):
#     data = get_object_or_404(Data, pk=pk)
#     prev_link = reverse('quarry:local_worker',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('quarry:machinery',
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

#     return render(request, 'quarry/data/worker/detail.html', context=context)


# def machinery_detail(request, pk):
#     data = get_object_or_404(Data, pk=pk)
#     prev_link = reverse('quarry:foreign_worker',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('quarry:daily_explosive',
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

#     return render(request, 'quarry/data/machinery/detail.html', context=context)


# def daily_explosive_detail(request, pk):
#     data = get_object_or_404(Data, pk=pk)
#     prev_link = reverse('quarry:machinery',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('quarry:energy_supply',
#                         kwargs={"pk": data.pk})
#     daily_explosive = get_object_or_404(DailyExplosive, data=data)

#     context = {
#         'title': 'Bahan Letupan Harian',
#         'daily_explosive': daily_explosive,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/data/daily_explosive/detail.html', context=context)


# def energy_supply_detail(request, pk):
#     data = get_object_or_404(Data, pk=pk)
#     prev_link = reverse('quarry:daily_explosive',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('quarry:operating_record',
#                         kwargs={"pk": data.pk})
#     energy_supply = get_object_or_404(EnergySupply, data=data)

#     context = {
#         'title': 'Bahan Tenaga',
#         'energy_supply': energy_supply,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/data/energy_supply/detail.html', context=context)


# def operating_record_detail(request, pk):
#     data = get_object_or_404(Data, pk=pk)
#     prev_link = reverse('quarry:energy_supply',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('quarry:royalties',
#                         kwargs={"pk": data.pk})
#     operating_record = get_object_or_404(
#         OperatingRecord, data=data)

#     context = {
#         'title': 'Rekod Operasi',
#         'operating_record': operating_record,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/data/operating_record/detail.html', context=context)


# def royalties_detail(request, pk):
#     data = get_object_or_404(Data, pk=pk)
#     prev_link = reverse('quarry:operating_record',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('quarry:other',
#                         kwargs={"pk": data.pk})
#     royalties = get_object_or_404(Royalties, data=data)

#     context = {
#         'title': 'Royalti',
#         'royalties': royalties,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/data/royalties/detail.html', context=context)


# def other_detail(request, pk):
#     data = get_object_or_404(Data, pk=pk)
#     prev_link = reverse('quarry:royalties',
#                         kwargs={"pk": data.pk})
#     other = get_object_or_404(Other, data=data)

#     context = {
#         'title': 'Lain-lain',
#         'other': other,
#         'prev_link': prev_link,
#         'data_id': data.id,
#     }

#     return render(request, 'quarry/data/other/detail.html', context=context)
