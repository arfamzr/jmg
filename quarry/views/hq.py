from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView

from account.models import User

from ..models import (
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
)


# data views
class DataSuccessListView(ListView):
    template_name = 'quarry/hq/data/success_list.html'
    model = Data
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()

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

    return render(request, 'quarry/hq/data/success_detail.html', context)


# class DataListView(ListView):
#     template_name = 'quarry/hq/miner_data/list.html'
#     model = Data
#     paginate_by = 10
#     ordering = ['-created_at']

#     def get_queryset(self):
#         queryset = super().get_queryset()

#         id_list = []
#         for data in queryset:
#             approval = data.get_last_approval()
#             if approval:
#                 if approval.state_approved == True and approval.admin_approved == True:
#                     id_list.append(data.id)
#         queryset = queryset.filter(id__in=id_list)

#         try:
#             name = self.request.GET['q']
#         except:
#             name = ''
#         if (name != ''):
#             # object_list = queryset.filter(location__icontains=name)
#             object_list = queryset
#         else:
#             object_list = queryset
#         return object_list

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = 'Senarai Data Kuari'
#         return context


# def miner_data_detail(request, pk):
#     miner_data = get_object_or_404(Data, pk=pk)
#     next_link = reverse('quarry:hq:production_statistic',
#                         kwargs={"pk": miner_data.pk})

#     context = {
#         'title': 'Data Kuari',
#         'miner_data': miner_data,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/hq/miner_data/detail.html', context=context)


# def production_statistic_detail(request, pk):
#     miner_data = get_object_or_404(Data, pk=pk)
#     prev_link = reverse('quarry:hq:miner_data',
#                         kwargs={"pk": miner_data.pk})
#     next_link = reverse('quarry:hq:sales_submission',
#                         kwargs={"pk": miner_data.pk})
#     production_statistic = get_object_or_404(
#         ProductionStatistic, miner_data=miner_data)

#     context = {
#         'title': 'Perangkaan Pengeluaran',
#         'production_statistic': production_statistic,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/hq/miner_data/production_statistic/detail.html', context=context)


# def sales_submission_detail(request, pk):
#     miner_data = get_object_or_404(Data, pk=pk)
#     prev_link = reverse('quarry:hq:production_statistic',
#                         kwargs={"pk": miner_data.pk})
#     next_link = reverse('quarry:hq:final_uses',
#                         kwargs={"pk": miner_data.pk})
#     sales_submission = get_object_or_404(
#         SalesSubmission, miner_data=miner_data)

#     context = {
#         'title': 'Penyerahan Jualan',
#         'sales_submission': sales_submission,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/hq/miner_data/sales_submission/detail.html', context=context)


# def final_uses_detail(request, pk):
#     miner_data = get_object_or_404(Data, pk=pk)
#     prev_link = reverse('quarry:hq:sales_submission',
#                         kwargs={"pk": miner_data.pk})
#     next_link = reverse('quarry:hq:local_worker',
#                         kwargs={"pk": miner_data.pk})
#     local_final_uses = get_object_or_404(LocalFinalUses, miner_data=miner_data)
#     export_final_uses = get_object_or_404(
#         ExportFinalUses, miner_data=miner_data)

#     context = {
#         'title': 'Kegunaan Akhir',
#         'local_final_uses': local_final_uses,
#         'export_final_uses': export_final_uses,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/hq/miner_data/final_uses/detail.html', context=context)


# def local_worker_detail(request, pk):
#     miner_data = get_object_or_404(Data, pk=pk)
#     prev_link = reverse('quarry:hq:final_uses',
#                         kwargs={"pk": miner_data.pk})
#     next_link = reverse('quarry:hq:foreign_worker',
#                         kwargs={"pk": miner_data.pk})
#     local_operator = get_object_or_404(LocalOperator, miner_data=miner_data)
#     local_contractor = get_object_or_404(
#         LocalContractor, miner_data=miner_data)

#     context = {
#         'title': 'Pekerjaan (Tempatan)',
#         'operator': local_operator,
#         'contractor': local_contractor,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/hq/miner_data/worker/detail.html', context=context)


# def foreign_worker_detail(request, pk):
#     miner_data = get_object_or_404(Data, pk=pk)
#     prev_link = reverse('quarry:hq:local_worker',
#                         kwargs={"pk": miner_data.pk})
#     next_link = reverse('quarry:hq:machinery',
#                         kwargs={"pk": miner_data.pk})
#     foreign_operator = get_object_or_404(
#         ForeignOperator, miner_data=miner_data)
#     foreign_contractor = get_object_or_404(
#         ForeignContractor, miner_data=miner_data)

#     context = {
#         'title': 'Pekerjaan (Asing)',
#         'operator': foreign_operator,
#         'contractor': foreign_contractor,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/hq/miner_data/worker/detail.html', context=context)


# def machinery_detail(request, pk):
#     miner_data = get_object_or_404(Data, pk=pk)
#     prev_link = reverse('quarry:hq:foreign_worker',
#                         kwargs={"pk": miner_data.pk})
#     next_link = reverse('quarry:hq:daily_explosive',
#                         kwargs={"pk": miner_data.pk})
#     combustion_machinery = get_object_or_404(
#         InternalCombustionMachinery, miner_data=miner_data)
#     electric_machinery = get_object_or_404(
#         ElectricMachinery, miner_data=miner_data)

#     context = {
#         'title': 'Jentera',
#         'combustion_machinery': combustion_machinery,
#         'electric_machinery': electric_machinery,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/hq/miner_data/machinery/detail.html', context=context)


# def daily_explosive_detail(request, pk):
#     miner_data = get_object_or_404(Data, pk=pk)
#     prev_link = reverse('quarry:hq:machinery',
#                         kwargs={"pk": miner_data.pk})
#     next_link = reverse('quarry:hq:energy_supply',
#                         kwargs={"pk": miner_data.pk})
#     daily_explosive = get_object_or_404(DailyExplosive, miner_data=miner_data)

#     context = {
#         'title': 'Bahan Letupan Harian',
#         'daily_explosive': daily_explosive,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/hq/miner_data/daily_explosive/detail.html', context=context)


# def energy_supply_detail(request, pk):
#     miner_data = get_object_or_404(Data, pk=pk)
#     prev_link = reverse('quarry:hq:daily_explosive',
#                         kwargs={"pk": miner_data.pk})
#     next_link = reverse('quarry:hq:operating_record',
#                         kwargs={"pk": miner_data.pk})
#     energy_supply = get_object_or_404(EnergySupply, miner_data=miner_data)

#     context = {
#         'title': 'Bahan Tenaga',
#         'energy_supply': energy_supply,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/hq/miner_data/energy_supply/detail.html', context=context)


# def operating_record_detail(request, pk):
#     miner_data = get_object_or_404(Data, pk=pk)
#     prev_link = reverse('quarry:hq:energy_supply',
#                         kwargs={"pk": miner_data.pk})
#     next_link = reverse('quarry:hq:royalties',
#                         kwargs={"pk": miner_data.pk})
#     operating_record = get_object_or_404(
#         OperatingRecord, miner_data=miner_data)

#     context = {
#         'title': 'Rekod Operasi',
#         'operating_record': operating_record,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/hq/miner_data/operating_record/detail.html', context=context)


# def royalties_detail(request, pk):
#     miner_data = get_object_or_404(Data, pk=pk)
#     prev_link = reverse('quarry:hq:operating_record',
#                         kwargs={"pk": miner_data.pk})
#     next_link = reverse('quarry:hq:other',
#                         kwargs={"pk": miner_data.pk})
#     royalties = get_object_or_404(Royalties, miner_data=miner_data)

#     context = {
#         'title': 'Royalti',
#         'royalties': royalties,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/hq/miner_data/royalties/detail.html', context=context)


# def other_detail(request, pk):
#     miner_data = get_object_or_404(Data, pk=pk)
#     prev_link = reverse('quarry:hq:royalties',
#                         kwargs={"pk": miner_data.pk})
#     other = get_object_or_404(Other, miner_data=miner_data)

#     context = {
#         'title': 'Lain-lain',
#         'other': other,
#         'prev_link': prev_link,
#     }

#     return render(request, 'quarry/hq/miner_data/other/detail.html', context=context)
