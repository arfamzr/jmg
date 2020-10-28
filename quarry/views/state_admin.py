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
from ..forms.state_admin import QuarryForm, QuarryMinerForm


class QuarryListView(ListView):
    template_name = 'quarry/state_admin/list.html'
    model = Quarry
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
        context["title"] = 'Senarai Kuari'
        return context


class QuarryCreateView(CreateView):
    template_name = 'quarry/state_admin/form.html'
    model = Quarry
    form_class = QuarryForm
    success_url = reverse_lazy('quarry:state_admin:list')

    def form_valid(self, form):
        form.instance.state = self.request.user.profile.state
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Tambah Kuari'
        return context


class QuarryUpdateView(UpdateView):
    template_name = 'quarry/state_admin/form.html'
    model = Quarry
    form_class = QuarryForm
    success_url = reverse_lazy('quarry:state_admin:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Update Kuari'
        return context


def toggle_active(request, pk):
    quarry = get_object_or_404(Quarry, pk=pk)
    if request.method == 'POST':
        if quarry.status == True:
            quarry.status = False
        else:
            quarry.status = True
        quarry.save()
        return redirect('quarry:state_admin:list')

    context = {
        'quarry': quarry,
    }

    return render(request, 'quarry/state_admin/toggle_active.html', context)


def quarry_detail(request, pk):
    quarry = get_object_or_404(Quarry, pk=pk)
    quarry_miner_list = QuarryMiner.objects.filter(quarry=quarry)

    try:
        name = request.GET['q']
    except:
        name = ''
    if (name != ''):
        quarry_miner_list = quarry_miner_list.filter(
            miner__username__icontains=name)

    page = request.GET.get('page', 1)

    paginator = Paginator(quarry_miner_list, 10)
    try:
        quarry_miner_list = paginator.page(page)
    except PageNotAnInteger:
        quarry_miner_list = paginator.page(1)
    except EmptyPage:
        quarry_miner_list = paginator.page(paginator.num_pages)

    context = {
        'quarry': quarry,
        'quarry_miner_list': quarry_miner_list,
        'title': 'Maklumat Kuari',
    }

    return render(request, 'quarry/state_admin/detail.html', context)


def add_miner(request, pk):
    quarry = get_object_or_404(Quarry, pk=pk)
    user_list = User.objects.all().filter(
        groups__name__in=['Industry'])

    try:
        name = request.GET['q']
    except:
        name = ''
    if (name != ''):
        user_list = user_list.filter(username__icontains=name)

    context = {
        'quarry': quarry,
        'user_list': user_list,
        'title': f'Tambah pengusaha "{quarry}"',
    }

    return render(request, 'quarry/state_admin/add_user.html', context)


def quarry_add_miner(request, quarry_pk, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    quarry = get_object_or_404(Quarry, pk=quarry_pk)

    if request.method == 'POST':
        form = QuarryMinerForm(request.POST)
        if form.is_valid():
            form.instance.miner = user
            form.instance.quarry = quarry
            form.instance.add_by = request.user
            form.save()

            return redirect('quarry:state_admin:detail', quarry.pk)

    else:
        form = QuarryMinerForm()

    context = {
        'each_user': user,
        'quarry': quarry,
        'form': form,
        'title': f'Tambah pengusaha({user}) ke "{quarry}"'
    }

    return render(request, 'quarry/state_admin/add_user_form.html', context)


def quarry_remove_miner(request, pk):
    quarry_miner = get_object_or_404(QuarryMiner, pk=pk)
    quarry_pk = quarry_miner.quarry.pk
    quarry_miner.delete()

    return redirect('quarry:state_admin:detail', quarry_pk)


def user_quarry_list(request, pk):
    user = get_object_or_404(User, pk=pk)
    quarry_miner_list = QuarryMiner.objects.filter(miner=user)

    page = request.GET.get('page', 1)

    paginator = Paginator(quarry_miner_list, 10)
    try:
        quarry_miner_list = paginator.page(page)
    except PageNotAnInteger:
        quarry_miner_list = paginator.page(1)
    except EmptyPage:
        quarry_miner_list = paginator.page(paginator.num_pages)

    context = {
        'each_user': user,
        'quarry_miner_list': quarry_miner_list,
        'title': 'Maklumat Pengguna',
    }

    return render(request, 'quarry/state_admin/list_user.html', context)


class QuarryMinerDataListView(ListView):
    template_name = 'quarry/state_admin/miner_data/list.html'
    model = QuarryMinerData
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
        context["title"] = 'Senarai Data Kuari'
        return context


class QuarryMinerDataSuccessListView(ListView):
    template_name = 'quarry/state_admin/miner_data/list.html'
    model = QuarryMinerData
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
        context["title"] = 'Senarai Data Kuari'
        return context


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
            notify_message = f'{data_approval.requestor} telah menghantar permohonan data untuk kuari "{miner_data.quarry}"'
            # hq/data_list belum ada
            notify_link = reverse('quarry:hq:data_list')

            for jmg_hq in jmg_hqs:
                notify.make_notify(jmg_hq, notify_message, notify_link)

        else:
            miner = data_approval.requestor
            state_inspector = data_approval.state_inspector

            notify = Notify()
            notify_message = f'Data untuk kuari "{miner_data.quarry}" telah ditolak'
            notify_link = reverse('quarry:data_list')
            state_notify_message = f'Data untuk kuari "{miner_data.quarry}"({miner}) telah ditolak'

            notify.make_notify(miner, notify_message, notify_link)
            notify.make_notify(state_inspector, state_notify_message)

        return redirect('quarry:state_admin:data_list')

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

    return render(request, 'quarry/state_admin/miner_data/detail.html', context)


# def miner_data_detail(request, pk):
#     miner_data = get_object_or_404(QuarryMinerData, pk=pk)
#     next_link = reverse('quarry:state_admin:production_statistic',
#                         kwargs={"pk": miner_data.pk})

#     context = {
#         'title': 'Data Kuari',
#         'miner_data': miner_data,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/state_admin/miner_data/detail.html', context=context)


def production_statistic_detail(request, pk):
    miner_data = get_object_or_404(QuarryMinerData, pk=pk)
    prev_link = reverse('quarry:state_admin:miner_data',
                        kwargs={"pk": miner_data.pk})
    next_link = reverse('quarry:state_admin:sales_submission',
                        kwargs={"pk": miner_data.pk})
    production_statistic = get_object_or_404(
        ProductionStatistic, miner_data=miner_data)

    context = {
        'title': 'Perangkaan Pengeluaran',
        'production_statistic': production_statistic,
        'prev_link': prev_link,
        'next_link': next_link,
    }

    return render(request, 'quarry/state_admin/miner_data/production_statistic/detail.html', context=context)


def sales_submission_detail(request, pk):
    miner_data = get_object_or_404(QuarryMinerData, pk=pk)
    prev_link = reverse('quarry:state_admin:production_statistic',
                        kwargs={"pk": miner_data.pk})
    next_link = reverse('quarry:state_admin:final_uses',
                        kwargs={"pk": miner_data.pk})
    sales_submission = get_object_or_404(
        SalesSubmission, miner_data=miner_data)

    context = {
        'title': 'Penyerahan Jualan',
        'sales_submission': sales_submission,
        'prev_link': prev_link,
        'next_link': next_link,
    }

    return render(request, 'quarry/state_admin/miner_data/sales_submission/detail.html', context=context)


def final_uses_detail(request, pk):
    miner_data = get_object_or_404(QuarryMinerData, pk=pk)
    prev_link = reverse('quarry:state_admin:sales_submission',
                        kwargs={"pk": miner_data.pk})
    next_link = reverse('quarry:state_admin:local_worker',
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

    return render(request, 'quarry/state_admin/miner_data/final_uses/detail.html', context=context)


def local_worker_detail(request, pk):
    miner_data = get_object_or_404(QuarryMinerData, pk=pk)
    prev_link = reverse('quarry:state_admin:final_uses',
                        kwargs={"pk": miner_data.pk})
    next_link = reverse('quarry:state_admin:foreign_worker',
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

    return render(request, 'quarry/state_admin/miner_data/worker/detail.html', context=context)


def foreign_worker_detail(request, pk):
    miner_data = get_object_or_404(QuarryMinerData, pk=pk)
    prev_link = reverse('quarry:state_admin:local_worker',
                        kwargs={"pk": miner_data.pk})
    next_link = reverse('quarry:state_admin:machinery',
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

    return render(request, 'quarry/state_admin/miner_data/worker/detail.html', context=context)


def machinery_detail(request, pk):
    miner_data = get_object_or_404(QuarryMinerData, pk=pk)
    prev_link = reverse('quarry:state_admin:foreign_worker',
                        kwargs={"pk": miner_data.pk})
    next_link = reverse('quarry:state_admin:daily_explosive',
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

    return render(request, 'quarry/state_admin/miner_data/machinery/detail.html', context=context)


def daily_explosive_detail(request, pk):
    miner_data = get_object_or_404(QuarryMinerData, pk=pk)
    prev_link = reverse('quarry:state_admin:machinery',
                        kwargs={"pk": miner_data.pk})
    next_link = reverse('quarry:state_admin:energy_supply',
                        kwargs={"pk": miner_data.pk})
    daily_explosive = get_object_or_404(DailyExplosive, miner_data=miner_data)

    context = {
        'title': 'Bahan Letupan Harian',
        'daily_explosive': daily_explosive,
        'prev_link': prev_link,
        'next_link': next_link,
    }

    return render(request, 'quarry/state_admin/miner_data/daily_explosive/detail.html', context=context)


def energy_supply_detail(request, pk):
    miner_data = get_object_or_404(QuarryMinerData, pk=pk)
    prev_link = reverse('quarry:state_admin:daily_explosive',
                        kwargs={"pk": miner_data.pk})
    next_link = reverse('quarry:state_admin:operating_record',
                        kwargs={"pk": miner_data.pk})
    energy_supply = get_object_or_404(EnergySupply, miner_data=miner_data)

    context = {
        'title': 'Bahan Tenaga',
        'energy_supply': energy_supply,
        'prev_link': prev_link,
        'next_link': next_link,
    }

    return render(request, 'quarry/state_admin/miner_data/energy_supply/detail.html', context=context)


def operating_record_detail(request, pk):
    miner_data = get_object_or_404(QuarryMinerData, pk=pk)
    prev_link = reverse('quarry:state_admin:energy_supply',
                        kwargs={"pk": miner_data.pk})
    next_link = reverse('quarry:state_admin:royalties',
                        kwargs={"pk": miner_data.pk})
    operating_record = get_object_or_404(
        OperatingRecord, miner_data=miner_data)

    context = {
        'title': 'Rekod Operasi',
        'operating_record': operating_record,
        'prev_link': prev_link,
        'next_link': next_link,
    }

    return render(request, 'quarry/state_admin/miner_data/operating_record/detail.html', context=context)


def royalties_detail(request, pk):
    miner_data = get_object_or_404(QuarryMinerData, pk=pk)
    prev_link = reverse('quarry:state_admin:operating_record',
                        kwargs={"pk": miner_data.pk})
    next_link = reverse('quarry:state_admin:other',
                        kwargs={"pk": miner_data.pk})
    royalties = get_object_or_404(Royalties, miner_data=miner_data)

    context = {
        'title': 'Royalti',
        'royalties': royalties,
        'prev_link': prev_link,
        'next_link': next_link,
    }

    return render(request, 'quarry/state_admin/miner_data/royalties/detail.html', context=context)


def other_detail(request, pk):
    miner_data = get_object_or_404(QuarryMinerData, pk=pk)
    prev_link = reverse('quarry:state_admin:royalties',
                        kwargs={"pk": miner_data.pk})
    other = get_object_or_404(Other, miner_data=miner_data)

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
            notify_message = f'{data_approval.requestor} telah menghantar permohonan data untuk kuari "{miner_data.quarry}"'
            # hq/data_list belum ada
            notify_link = reverse('quarry:hq:data_list')

            for jmg_hq in jmg_hqs:
                notify.make_notify(jmg_hq, notify_message, notify_link)

        else:
            miner = data_approval.requestor
            state_inspector = data_approval.state_inspector

            notify = Notify()
            notify_message = f'Data untuk kuari "{miner_data.quarry}" telah ditolak'
            notify_link = reverse('quarry:data_list')
            state_notify_message = f'Data untuk kuari "{miner_data.quarry}"({miner}) telah ditolak'

            notify.make_notify(miner, notify_message, notify_link)
            notify.make_notify(state_inspector, state_notify_message)

        return redirect('quarry:state_admin:data_list')

    context = {
        'title': 'Lain-lain',
        'other': other,
        'prev_link': prev_link,
        'miner_data_id': miner_data.id,
    }

    return render(request, 'quarry/state_admin/miner_data/other/detail.html', context=context)


def quarry_graph(request, pk):
    miner_data = get_object_or_404(QuarryMinerData, pk=pk)
    rock_type = miner_data.quarry.main_rock_type
    rock_list = QuarryDataApproval.objects.filter(miner_data=miner_data)

    def get_rock_list(rock_list):
        rock_jan_list = rock_list.filter(
            miner_data__month=1)
        rock_jan_production = 0
        rock_jan_royalties = 0
        for rock in rock_jan_list:
            rock_jan_production += rock.miner_data.productionstatistic.main_rock_production
            rock_jan_royalties += rock.miner_data.royalties.royalties

        rock_feb_list = rock_list.filter(
            miner_data__month=2)
        rock_feb_production = 0
        rock_feb_royalties = 0
        for rock in rock_feb_list:
            rock_feb_production += rock.miner_data.productionstatistic.main_rock_production
            rock_feb_royalties += rock.miner_data.royalties.royalties

        rock_mac_list = rock_list.filter(
            miner_data__month=3)
        rock_mac_production = 0
        rock_mac_royalties = 0
        for rock in rock_mac_list:
            rock_mac_production += rock.miner_data.productionstatistic.main_rock_production
            rock_mac_royalties += rock.miner_data.royalties.royalties

        rock_apr_list = rock_list.filter(
            miner_data__month=4)
        rock_apr_production = 0
        rock_apr_royalties = 0
        for rock in rock_apr_list:
            rock_apr_production += rock.miner_data.productionstatistic.main_rock_production
            rock_apr_royalties += rock.miner_data.royalties.royalties

        rock_mei_list = rock_list.filter(
            miner_data__month=5)
        rock_mei_production = 0
        rock_mei_royalties = 0
        for rock in rock_mei_list:
            rock_mei_production += rock.miner_data.productionstatistic.main_rock_production
            rock_mei_royalties += rock.miner_data.royalties.royalties

        rock_jun_list = rock_list.filter(
            miner_data__month=6)
        rock_jun_production = 0
        rock_jun_royalties = 0
        for rock in rock_jun_list:
            rock_jun_production += rock.miner_data.productionstatistic.main_rock_production
            rock_jun_royalties += rock.miner_data.royalties.royalties

        rock_jul_list = rock_list.filter(
            miner_data__month=7)
        rock_jul_production = 0
        rock_jul_royalties = 0
        for rock in rock_jul_list:
            rock_jul_production += rock.miner_data.productionstatistic.main_rock_production
            rock_jul_royalties += rock.miner_data.royalties.royalties

        rock_ogos_list = rock_list.filter(
            miner_data__month=8)
        rock_ogos_production = 0
        rock_ogos_royalties = 0
        for rock in rock_ogos_list:
            rock_ogos_production += rock.miner_data.productionstatistic.main_rock_production
            rock_ogos_royalties += rock.miner_data.royalties.royalties

        rock_sep_list = rock_list.filter(
            miner_data__month=9)
        rock_sep_production = 0
        rock_sep_royalties = 0
        for rock in rock_sep_list:
            rock_sep_production += rock.miner_data.productionstatistic.main_rock_production
            rock_sep_royalties += rock.miner_data.royalties.royalties

        rock_okt_list = rock_list.filter(
            miner_data__month=10)
        rock_okt_production = 0
        rock_okt_royalties = 0
        for rock in rock_okt_list:
            rock_okt_production += rock.miner_data.productionstatistic.main_rock_production
            rock_okt_royalties += rock.miner_data.royalties.royalties

        rock_nov_list = rock_list.filter(
            miner_data__month=11)
        rock_nov_production = 0
        rock_nov_royalties = 0
        for rock in rock_nov_list:
            rock_nov_production += rock.miner_data.productionstatistic.main_rock_production
            rock_nov_royalties += rock.miner_data.royalties.royalties

        rock_dis_list = rock_list.filter(
            miner_data__month=12)
        rock_dis_production = 0
        rock_dis_royalties = 0
        for rock in rock_dis_list:
            rock_dis_production += rock.miner_data.productionstatistic.main_rock_production
            rock_dis_royalties += rock.miner_data.royalties.royalties

        rock = {
            'jan': {
                'production': rock_jan_production,
                'royalties': rock_jan_royalties,
            },
            'feb': {
                'production': rock_feb_production,
                'royalties': rock_feb_royalties,
            },
            'mac': {
                'production': rock_mac_production,
                'royalties': rock_mac_royalties,
            },
            'apr': {
                'production': rock_apr_production,
                'royalties': rock_apr_royalties,
            },
            'mei': {
                'production': rock_mei_production,
                'royalties': rock_mei_royalties,
            },
            'jun': {
                'production': rock_jun_production,
                'royalties': rock_jun_royalties,
            },
            'jul': {
                'production': rock_jul_production,
                'royalties': rock_jul_royalties,
            },
            'ogos': {
                'production': rock_ogos_production,
                'royalties': rock_ogos_royalties,
            },
            'sep': {
                'production': rock_sep_production,
                'royalties': rock_sep_royalties,
            },
            'okt': {
                'production': rock_okt_production,
                'royalties': rock_okt_royalties,
            },
            'nov': {
                'production': rock_nov_production,
                'royalties': rock_nov_royalties,
            },
            'dis': {
                'production': rock_dis_production,
                'royalties': rock_dis_royalties,
            },
        }

        return rock

    rock = get_rock_list(rock_list)

    months = [
        {
            'name': 'JANUARI',
            'rock': rock['jan'],
        },
        {
            'name': 'FEBRUARI',
            'rock': rock['feb'],
        },
        {
            'name': 'MAC',
            'rock': rock['mac'],
        },
        {
            'name': 'APRIL',
            'rock': rock['apr'],
        },
        {
            'name': 'MEI',
            'rock': rock['mei'],
        },
        {
            'name': 'JUN',
            'rock': rock['jun'],
        },
        {
            'name': 'JULAI',
            'rock': rock['jul'],
        },
        {
            'name': 'OGOS',
            'rock': rock['ogos'],
        },
        {
            'name': 'SEPTEMBER',
            'rock': rock['sep'],
        },
        {
            'name': 'OKTOBER',
            'rock': rock['okt'],
        },
        {
            'name': 'NOVEMBER',
            'rock': rock['nov'],
        },
        {
            'name': 'DISEMBER',
            'rock': rock['dis'],
        },
    ]

    rocks = {
        'name': rock_type,
        'production': sum([month['rock']['production'] for month in months]),
        'royalties': sum([month['rock']['royalties'] for month in months]),
    }

    context = {
        'title': 'Laporan/Graph Kuari',
        'rock': rocks,
        'months': months,
    }

    return render(request, 'quarry/state_admin/graph/data.html', context)
