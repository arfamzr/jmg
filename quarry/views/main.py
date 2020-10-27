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
    QuarryMiner,
    QuarryMinerData,
    ProductionStatistic,
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
    QuarryDataApproval,
)
from ..forms.main import (
    QuarryMinerDataForm,
    ProductionStatisticForm,
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


class QuarryMinerListView(ListView):
    template_name = 'quarry/list.html'
    model = QuarryMiner
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
        context["title"] = 'Senarai Kuari'
        return context


class QuarryMinerDataListView(ListView):
    template_name = 'quarry/miner_data/list.html'
    model = QuarryMinerData
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
        context["title"] = 'Senarai Data Kuari'
        return context


def add_report(request, pk):
    quarry_miner = get_object_or_404(QuarryMiner, pk=pk)

    if request.method == 'POST':
        form = QuarryMinerDataForm(request.POST)
        if form.is_valid():
            form.instance.miner = quarry_miner
            form.instance.quarry = quarry_miner.quarry
            form.instance.state = quarry_miner.quarry.state
            miner_data = form.save()

            return redirect('quarry:production_statistic_edit', pk=miner_data.id)

    else:
        form = QuarryMinerDataForm()

    context = {
        'form': form,
        'title': 'Tambah Data Kuari',
    }

    return render(request, 'quarry/miner_data/form.html', context)


def production_statistic_edit(request, pk):
    miner_data = get_object_or_404(QuarryMinerData, pk=pk)
    try:
        production_statistic = ProductionStatistic.objects.get(
            miner_data=miner_data)
    except ProductionStatistic.DoesNotExist:
        production_statistic = None

    if request.method == 'POST':
        if production_statistic == None:
            form = ProductionStatisticForm(request.POST)
        else:
            form = ProductionStatisticForm(
                request.POST, instance=production_statistic)

        if form.is_valid():
            form.instance.miner_data = miner_data
            form.save()
            return redirect('quarry:sales_submission_edit', pk=miner_data.pk)

    else:
        if production_statistic == None:
            form = ProductionStatisticForm()
        else:
            form = ProductionStatisticForm(instance=production_statistic)

    context = {
        'title': 'Edit Perangkaan Pengeluaran',
        'form': form,
    }

    return render(request, 'quarry/miner_data/production_statistic/form.html', context=context)


def sales_submission_edit(request, pk):
    miner_data = get_object_or_404(QuarryMinerData, pk=pk)
    prev_link = reverse('quarry:production_statistic_edit',
                        kwargs={"pk": miner_data.pk})
    try:
        sales_submission = SalesSubmission.objects.get(miner_data=miner_data)
    except SalesSubmission.DoesNotExist:
        sales_submission = None

    if request.method == 'POST':
        if sales_submission == None:
            form = SalesSubmissionForm(request.POST)
        else:
            form = SalesSubmissionForm(
                request.POST, instance=sales_submission)

        if form.is_valid():
            form.instance.miner_data = miner_data
            form.save()
            return redirect('quarry:final_uses_edit', pk=miner_data.pk)

    else:
        if sales_submission == None:
            form = SalesSubmissionForm()
        else:
            form = SalesSubmissionForm(instance=sales_submission)

    context = {
        'title': 'Edit Penyerahan Jualan',
        'form': form,
        'prev_link': prev_link,
    }

    return render(request, 'quarry/miner_data/sales_submission/form.html', context=context)


def final_uses_edit(request, pk):
    miner_data = get_object_or_404(QuarryMinerData, pk=pk)
    prev_link = reverse('quarry:sales_submission_edit',
                        kwargs={"pk": miner_data.pk})
    try:
        local_final_uses = LocalFinalUses.objects.get(miner_data=miner_data)
        export_final_uses = ExportFinalUses.objects.get(miner_data=miner_data)
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
            local_form.instance.miner_data = miner_data
            export_form.instance.miner_data = miner_data
            local_form.save()
            export_form.save()
            return redirect('quarry:local_worker_edit', pk=miner_data.pk)

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

    return render(request, 'quarry/miner_data/final_uses/form.html', context=context)


def local_worker_edit(request, pk):
    miner_data = get_object_or_404(QuarryMinerData, pk=pk)
    prev_link = reverse('quarry:final_uses_edit',
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
            return redirect('quarry:foreign_worker_edit', pk=miner_data.pk)

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

    return render(request, 'quarry/miner_data/worker/form.html', context=context)


def foreign_worker_edit(request, pk):
    miner_data = get_object_or_404(QuarryMinerData, pk=pk)
    prev_link = reverse('quarry:local_worker_edit',
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
            return redirect('quarry:machinery_edit', pk=miner_data.pk)

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

    return render(request, 'quarry/miner_data/worker/form.html', context=context)


def machinery_edit(request, pk):
    miner_data = get_object_or_404(QuarryMinerData, pk=pk)
    prev_link = reverse('quarry:foreign_worker_edit',
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
            return redirect('quarry:daily_explosive_edit', pk=miner_data.pk)

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

    return render(request, 'quarry/miner_data/machinery/form.html', context=context)


def daily_explosive_edit(request, pk):
    miner_data = get_object_or_404(QuarryMinerData, pk=pk)
    prev_link = reverse('quarry:machinery_edit',
                        kwargs={"pk": miner_data.pk})
    try:
        daily_explosive = DailyExplosive.objects.get(miner_data=miner_data)
    except DailyExplosive.DoesNotExist:
        daily_explosive = None

    if request.method == 'POST':
        if daily_explosive == None:
            form = DailyExplosiveForm(request.POST)
        else:
            form = DailyExplosiveForm(
                request.POST, instance=daily_explosive)

        if form.is_valid():
            form.instance.miner_data = miner_data
            form.save()
            return redirect('quarry:energy_supply_edit', pk=miner_data.pk)

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

    return render(request, 'quarry/miner_data/daily_explosive/form.html', context=context)


def energy_supply_edit(request, pk):
    miner_data = get_object_or_404(QuarryMinerData, pk=pk)
    prev_link = reverse('quarry:daily_explosive_edit',
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
            return redirect('quarry:operating_record_edit', pk=miner_data.pk)

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

    return render(request, 'quarry/miner_data/energy_supply/form.html', context=context)


def operating_record_edit(request, pk):
    miner_data = get_object_or_404(QuarryMinerData, pk=pk)
    prev_link = reverse('quarry:energy_supply_edit',
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
            return redirect('quarry:royalties_edit', pk=miner_data.pk)

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

    return render(request, 'quarry/miner_data/operating_record/form.html', context=context)


def royalties_edit(request, pk):
    miner_data = get_object_or_404(QuarryMinerData, pk=pk)
    prev_link = reverse('quarry:operating_record_edit',
                        kwargs={"pk": miner_data.pk})
    try:
        royalties = Royalties.objects.get(miner_data=miner_data)
    except Royalties.DoesNotExist:
        royalties = None

    if request.method == 'POST':
        if royalties == None:
            form = RoyaltiesForm(request.POST)
        else:
            form = RoyaltiesForm(
                request.POST, instance=royalties)

        if form.is_valid():
            form.instance.miner_data = miner_data
            form.save()
            return redirect('quarry:other_edit', pk=miner_data.pk)

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

    return render(request, 'quarry/miner_data/royalties/form.html', context=context)


def other_edit(request, pk):
    miner_data = get_object_or_404(QuarryMinerData, pk=pk)
    prev_link = reverse('quarry:royalties_edit',
                        kwargs={"pk": miner_data.pk})
    try:
        other = Other.objects.get(miner_data=miner_data)
    except Other.DoesNotExist:
        other = None

    if request.method == 'POST':
        if other == None:
            form = OtherForm(request.POST)
        else:
            form = OtherForm(
                request.POST, instance=other)

        if form.is_valid():
            form.instance.miner_data = miner_data
            form.save()
            data_approval = QuarryDataApproval.objects.create(
                miner_data=miner_data, requestor=request.user)

            jmg_states = User.objects.filter(
                groups__name='JMG State', profile__state=miner_data.state)

            notify = Notify()
            notify_message = f'{request.user} telah menghantar permohonan data untuk kuari "{miner_data.quarry}"'
            notify_link = reverse('quarry:state:data_list')

            for jmg_state in jmg_states:
                notify.make_notify(jmg_state, notify_message, notify_link)

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

    return render(request, 'quarry/miner_data/other/form.html', context=context)


def miner_data_delete(request, pk):
    miner_data = get_object_or_404(QuarryMinerData, pk=pk)

    if miner_data.miner.miner == request.user:
        miner_data.delete()

    return redirect('quarry:data_list')


def miner_data_detail(request, pk):
    miner_data = get_object_or_404(QuarryMinerData, pk=pk)
    production_statistic = get_object_or_404(
        ProductionStatistic, miner_data=miner_data)
    sales_submission = get_object_or_404(
        SalesSubmission, miner_data=miner_data)
    local_final_uses = get_object_or_404(LocalFinalUses, miner_data=miner_data)
    export_final_uses = get_object_or_404(
        ExportFinalUses, miner_data=miner_data)
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
    daily_explosive = get_object_or_404(DailyExplosive, miner_data=miner_data)
    energy_supply = get_object_or_404(EnergySupply, miner_data=miner_data)
    operating_record = get_object_or_404(
        OperatingRecord, miner_data=miner_data)
    royalties = get_object_or_404(Royalties, miner_data=miner_data)
    other = get_object_or_404(Other, miner_data=miner_data)

    context = {
        'title': 'Data Kuari',
        'miner_data': miner_data,
        'production_statistic': production_statistic,
        'sales_submission': sales_submission,
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

    return render(request, 'quarry/miner_data/detail.html', context)


# def miner_data_detail(request, pk):
#     miner_data = get_object_or_404(QuarryMinerData, pk=pk)
#     next_link = reverse('quarry:production_statistic',
#                         kwargs={"pk": miner_data.pk})

#     context = {
#         'title': 'Data Kuari',
#         'miner_data': miner_data,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/miner_data/detail.html', context=context)


def production_statistic_detail(request, pk):
    miner_data = get_object_or_404(QuarryMinerData, pk=pk)
    prev_link = reverse('quarry:miner_data',
                        kwargs={"pk": miner_data.pk})
    next_link = reverse('quarry:sales_submission',
                        kwargs={"pk": miner_data.pk})
    production_statistic = get_object_or_404(
        ProductionStatistic, miner_data=miner_data)

    context = {
        'title': 'Perangkaan Pengeluaran',
        'production_statistic': production_statistic,
        'prev_link': prev_link,
        'next_link': next_link,
    }

    return render(request, 'quarry/miner_data/production_statistic/detail.html', context=context)


def sales_submission_detail(request, pk):
    miner_data = get_object_or_404(QuarryMinerData, pk=pk)
    prev_link = reverse('quarry:production_statistic',
                        kwargs={"pk": miner_data.pk})
    next_link = reverse('quarry:final_uses',
                        kwargs={"pk": miner_data.pk})
    sales_submission = get_object_or_404(
        SalesSubmission, miner_data=miner_data)

    context = {
        'title': 'Penyerahan Jualan',
        'sales_submission': sales_submission,
        'prev_link': prev_link,
        'next_link': next_link,
    }

    return render(request, 'quarry/miner_data/sales_submission/detail.html', context=context)


def final_uses_detail(request, pk):
    miner_data = get_object_or_404(QuarryMinerData, pk=pk)
    prev_link = reverse('quarry:sales_submission',
                        kwargs={"pk": miner_data.pk})
    next_link = reverse('quarry:local_worker',
                        kwargs={"pk": miner_data.pk})
    local_final_uses = get_object_or_404(LocalFinalUses, miner_data=miner_data)
    export_final_uses = get_object_or_404(
        ExportFinalUses, miner_data=miner_data)

    context = {
        'title': 'Kegunaan Akhir',
        'local_final_uses': local_final_uses,
        'export_final_uses': export_final_uses,
        'prev_link': prev_link,
        'next_link': next_link,
    }

    return render(request, 'quarry/miner_data/final_uses/detail.html', context=context)


def local_worker_detail(request, pk):
    miner_data = get_object_or_404(QuarryMinerData, pk=pk)
    prev_link = reverse('quarry:final_uses',
                        kwargs={"pk": miner_data.pk})
    next_link = reverse('quarry:foreign_worker',
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

    return render(request, 'quarry/miner_data/worker/detail.html', context=context)


def foreign_worker_detail(request, pk):
    miner_data = get_object_or_404(QuarryMinerData, pk=pk)
    prev_link = reverse('quarry:local_worker',
                        kwargs={"pk": miner_data.pk})
    next_link = reverse('quarry:machinery',
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

    return render(request, 'quarry/miner_data/worker/detail.html', context=context)


def machinery_detail(request, pk):
    miner_data = get_object_or_404(QuarryMinerData, pk=pk)
    prev_link = reverse('quarry:foreign_worker',
                        kwargs={"pk": miner_data.pk})
    next_link = reverse('quarry:daily_explosive',
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

    return render(request, 'quarry/miner_data/machinery/detail.html', context=context)


def daily_explosive_detail(request, pk):
    miner_data = get_object_or_404(QuarryMinerData, pk=pk)
    prev_link = reverse('quarry:machinery',
                        kwargs={"pk": miner_data.pk})
    next_link = reverse('quarry:energy_supply',
                        kwargs={"pk": miner_data.pk})
    daily_explosive = get_object_or_404(DailyExplosive, miner_data=miner_data)

    context = {
        'title': 'Bahan Letupan Harian',
        'daily_explosive': daily_explosive,
        'prev_link': prev_link,
        'next_link': next_link,
    }

    return render(request, 'quarry/miner_data/daily_explosive/detail.html', context=context)


def energy_supply_detail(request, pk):
    miner_data = get_object_or_404(QuarryMinerData, pk=pk)
    prev_link = reverse('quarry:daily_explosive',
                        kwargs={"pk": miner_data.pk})
    next_link = reverse('quarry:operating_record',
                        kwargs={"pk": miner_data.pk})
    energy_supply = get_object_or_404(EnergySupply, miner_data=miner_data)

    context = {
        'title': 'Bahan Tenaga',
        'energy_supply': energy_supply,
        'prev_link': prev_link,
        'next_link': next_link,
    }

    return render(request, 'quarry/miner_data/energy_supply/detail.html', context=context)


def operating_record_detail(request, pk):
    miner_data = get_object_or_404(QuarryMinerData, pk=pk)
    prev_link = reverse('quarry:energy_supply',
                        kwargs={"pk": miner_data.pk})
    next_link = reverse('quarry:royalties',
                        kwargs={"pk": miner_data.pk})
    operating_record = get_object_or_404(
        OperatingRecord, miner_data=miner_data)

    context = {
        'title': 'Rekod Operasi',
        'operating_record': operating_record,
        'prev_link': prev_link,
        'next_link': next_link,
    }

    return render(request, 'quarry/miner_data/operating_record/detail.html', context=context)


def royalties_detail(request, pk):
    miner_data = get_object_or_404(QuarryMinerData, pk=pk)
    prev_link = reverse('quarry:operating_record',
                        kwargs={"pk": miner_data.pk})
    next_link = reverse('quarry:other',
                        kwargs={"pk": miner_data.pk})
    royalties = get_object_or_404(Royalties, miner_data=miner_data)

    context = {
        'title': 'Royalti',
        'royalties': royalties,
        'prev_link': prev_link,
        'next_link': next_link,
    }

    return render(request, 'quarry/miner_data/royalties/detail.html', context=context)


def other_detail(request, pk):
    miner_data = get_object_or_404(QuarryMinerData, pk=pk)
    prev_link = reverse('quarry:royalties',
                        kwargs={"pk": miner_data.pk})
    other = get_object_or_404(Other, miner_data=miner_data)

    context = {
        'title': 'Lain-lain',
        'other': other,
        'prev_link': prev_link,
        'miner_data_id': miner_data.id,
    }

    return render(request, 'quarry/miner_data/other/detail.html', context=context)


def get_comment_data(request, pk):
    data_miner = get_object_or_404(QuarryMinerData, pk=pk)
    data_approval = data_miner.get_last_approval()
    if data_approval.admin_comment:
        return HttpResponse(data_approval.admin_comment)
    elif data_approval.state_comment:
        return HttpResponse(data_approval.state_comment)
    else:
        return HttpResponse('')
