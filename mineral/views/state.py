from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView

from account.models import User
from account.user_check import user_is_jmg_state, UserIsJMGStateMixin
from notification.notify import Notify

from ..models import (
    ProcessFactory,
    ProcessManager,
    ProcessData,
    ProcessStatistic,
    ProcessSubmission,
    LocalOperator,
    LocalContractor,
    ForeignOperator,
    ForeignContractor,
    InternalCombustionMachinery,
    ElectricMachinery,
    EnergySupply,
    OperatingRecord,
    Other,
    Approval,
)


# data views
class DataListView(UserIsJMGStateMixin, ListView):
    template_name = 'mineral/state/data/list.html'
    model = ProcessData
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
        context["title"] = 'Senarai Data Proses Mineral'
        return context


@user_is_jmg_state()
def data_detail(request, pk):
    data = get_object_or_404(ProcessData, pk=pk)
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

        # noted here
        # if approved:
        #     jmg_state_admins = User.objects.filter(
        #         groups__name='JMG State Admin', profile__state=data.state)

        #     notify = Notify()
        #     notify_message = f'{data_approval.requestor} telah menghantar permohonan data untuk kuari "{data.mineral}"'
        #     notify_link = reverse('mineral:state_admin:data_list')

        #     for jmg_state_admin in jmg_state_admins:
        #         notify.make_notify(
        #             jmg_state_admin, notify_message, notify_link)
        # else:
        #     miner = data_approval.requestor

        #     notify = Notify()
        #     notify_message = f'Data untuk kuari "{data.mineral}" telah ditolak'
        #     notify_link = reverse('mineral:data_list')

        #     notify.make_notify(miner, notify_message, notify_link)

        return redirect('mineral:state:data_list')

    context = {
        'title': 'Data Proses Mineral',
        'data': data,
        'local_operator': local_operator,
        'local_contractor': local_contractor,
        'foreign_operator': foreign_operator,
        'foreign_contractor': foreign_contractor,
        'combustion_machinery': combustion_machinery,
        'electric_machinery': electric_machinery,
        'energy_supply': energy_supply,
        'operating_record': operating_record,
        'other': other,
        'other': other,
    }

    return render(request, 'mineral/state/data/detail.html', context)
