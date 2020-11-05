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
    Quarry,
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
class DataListView(ListView):
    template_name = 'quarry/state/data/list.html'
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
        context["title"] = 'Senarai PKB'
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
        data_approval.state_inspector = request.user
        data_approval.state_comment = request.POST.get('comment', '')
        data_approval.state_approved = approved
        data_approval.save()

        # if approved:
        #     jmg_state_admins = User.objects.filter(
        #         groups__name='JMG State Admin', profile__state=data.state)

        #     notify = Notify()
        #     notify_message = f'{data.miner.quarry} telah menghantar permohonan data untuk kuari "{data.quarry}"'
        #     notify_link = reverse('quarry:state_admin:data_list')

        #     for jmg_state_admin in jmg_state_admins:
        #         notify.make_notify(
        #             jmg_state_admin, notify_message, notify_link)
        # else:
        #     miner = data_approval.requestor

        #     notify = Notify()
        #     notify_message = f'Data untuk kuari "{data.quarry}" telah ditolak'
        #     notify_link = reverse('quarry:data_list')

        #     notify.make_notify(miner, notify_message, notify_link)

        return redirect('quarry:state:data_list')

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

    return render(request, 'quarry/state/data/detail.html', context)


# class QuarryListView(ListView):
#     template_name = 'quarry/state/list.html'
#     model = Quarry
#     paginate_by = 10
#     ordering = ['-created_at']

#     def get_queryset(self):
#         queryset = super().get_queryset().filter(
#             state=self.request.user.profile.state)
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

#     return render(request, 'quarry/state/detail.html', context)


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

#     return render(request, 'quarry/state/list_user.html', context)


# # def data_detail(request, pk):
# #     data = get_object_or_404(QuarryMinerData, pk=pk)
# #     next_link = reverse('quarry:state:production_statistic',
# #                         kwargs={"pk": data.pk})

# #     context = {
# #         'title': 'Data Kuari',
# #         'data': data,
# #         'next_link': next_link,
# #     }

# #     return render(request, 'quarry/state/data/detail.html', context=context)


# def production_statistic_detail(request, pk):
#     data = get_object_or_404(QuarryMinerData, pk=pk)
#     prev_link = reverse('quarry:state:data',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('quarry:state:sales_submission',
#                         kwargs={"pk": data.pk})
#     production_statistic = get_object_or_404(
#         ProductionStatistic, data=data)

#     context = {
#         'title': 'Perangkaan Pengeluaran',
#         'production_statistic': production_statistic,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/state/data/production_statistic/detail.html', context=context)


# def sales_submission_detail(request, pk):
#     data = get_object_or_404(QuarryMinerData, pk=pk)
#     prev_link = reverse('quarry:state:production_statistic',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('quarry:state:final_uses',
#                         kwargs={"pk": data.pk})
#     sales_submission = get_object_or_404(
#         SalesSubmission, data=data)

#     context = {
#         'title': 'Penyerahan Jualan',
#         'sales_submission': sales_submission,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/state/data/sales_submission/detail.html', context=context)


# def final_uses_detail(request, pk):
#     data = get_object_or_404(QuarryMinerData, pk=pk)
#     prev_link = reverse('quarry:state:sales_submission',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('quarry:state:local_worker',
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

#     return render(request, 'quarry/state/data/final_uses/detail.html', context=context)


# def local_worker_detail(request, pk):
#     data = get_object_or_404(QuarryMinerData, pk=pk)
#     prev_link = reverse('quarry:state:final_uses',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('quarry:state:foreign_worker',
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

#     return render(request, 'quarry/state/data/worker/detail.html', context=context)


# def foreign_worker_detail(request, pk):
#     data = get_object_or_404(QuarryMinerData, pk=pk)
#     prev_link = reverse('quarry:state:local_worker',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('quarry:state:machinery',
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

#     return render(request, 'quarry/state/data/worker/detail.html', context=context)


# def machinery_detail(request, pk):
#     data = get_object_or_404(QuarryMinerData, pk=pk)
#     prev_link = reverse('quarry:state:foreign_worker',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('quarry:state:daily_explosive',
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

#     return render(request, 'quarry/state/data/machinery/detail.html', context=context)


# def daily_explosive_detail(request, pk):
#     data = get_object_or_404(QuarryMinerData, pk=pk)
#     prev_link = reverse('quarry:state:machinery',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('quarry:state:energy_supply',
#                         kwargs={"pk": data.pk})
#     daily_explosive = get_object_or_404(DailyExplosive, data=data)

#     context = {
#         'title': 'Bahan Letupan Harian',
#         'daily_explosive': daily_explosive,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/state/data/daily_explosive/detail.html', context=context)


# def energy_supply_detail(request, pk):
#     data = get_object_or_404(QuarryMinerData, pk=pk)
#     prev_link = reverse('quarry:state:daily_explosive',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('quarry:state:operating_record',
#                         kwargs={"pk": data.pk})
#     energy_supply = get_object_or_404(EnergySupply, data=data)

#     context = {
#         'title': 'Bahan Tenaga',
#         'energy_supply': energy_supply,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/state/data/energy_supply/detail.html', context=context)


# def operating_record_detail(request, pk):
#     data = get_object_or_404(QuarryMinerData, pk=pk)
#     prev_link = reverse('quarry:state:energy_supply',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('quarry:state:royalties',
#                         kwargs={"pk": data.pk})
#     operating_record = get_object_or_404(
#         OperatingRecord, data=data)

#     context = {
#         'title': 'Rekod Operasi',
#         'operating_record': operating_record,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/state/data/operating_record/detail.html', context=context)


# def royalties_detail(request, pk):
#     data = get_object_or_404(QuarryMinerData, pk=pk)
#     prev_link = reverse('quarry:state:operating_record',
#                         kwargs={"pk": data.pk})
#     next_link = reverse('quarry:state:other',
#                         kwargs={"pk": data.pk})
#     royalties = get_object_or_404(Royalties, data=data)

#     context = {
#         'title': 'Royalti',
#         'royalties': royalties,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/state/data/royalties/detail.html', context=context)


# def other_detail(request, pk):
#     data = get_object_or_404(QuarryMinerData, pk=pk)
#     prev_link = reverse('quarry:state:royalties',
#                         kwargs={"pk": data.pk})
#     other = get_object_or_404(Other, data=data)

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
#             notify_message = f'{data.miner.quarry} telah menghantar permohonan data untuk kuari "{data.quarry}"'
#             notify_link = reverse('quarry:state_admin:data_list')

#             for jmg_state_admin in jmg_state_admins:
#                 notify.make_notify(
#                     jmg_state_admin, notify_message, notify_link)
#         else:
#             miner = data_approval.requestor

#             notify = Notify()
#             notify_message = f'Data untuk kuari "{data.quarry}" telah ditolak'
#             notify_link = reverse('quarry:data_list')

#             notify.make_notify(miner, notify_message, notify_link)

#         return redirect('quarry:state:data_list')

#     context = {
#         'title': 'Lain-lain',
#         'other': other,
#         'prev_link': prev_link,
#         'data_id': data.id,
#     }

#     return render(request, 'quarry/state/data/other/detail.html', context=context)
