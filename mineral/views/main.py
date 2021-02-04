from django.db.models import manager
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, FormView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView

from account.models import User
from account.user_check import user_is_manager, UserIsManagerMixin
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
from ..forms.main import (
    DataForm,
    ProcessStatisticForm,
    ProcessSubmissionForm,
    LocalOperatorForm,
    LocalContractorForm,
    ForeignOperatorForm,
    ForeignContractorForm,
    InternalCombustionMachineryForm,
    ElectricMachineryForm,
    EnergySupplyForm,
    OperatingRecordForm,
    OtherForm,
)


# data views
class DataListView(UserIsManagerMixin, ListView):
    template_name = 'mineral/data/list.html'
    model = ProcessData
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
        context["title"] = 'Senarai Lesen Memproses Mineral'
        return context


class DataCreateView(UserIsManagerMixin, CreateView):
    model = ProcessData
    form_class = DataForm
    template_name = 'mineral/data/form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['manager'] = self.request.user.processmanager
        return kwargs

    def form_valid(self, form):
        form.instance.manager = self.request.user.processmanager
        form.instance.factory = self.request.user.processmanager.factory
        form.instance.state = self.request.user.processmanager.factory.state
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mineral:process_statistic_edit', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Tambah Lesen Memproses Mineral'
        return context


@user_is_manager()
def data_delete(request, pk):
    if request.method == 'POST':
        data = get_object_or_404(ProcessData, pk=pk)

        if data.manager.user == request.user:
            data.delete()

    return redirect('mineral:data_list')


@user_is_manager()
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

    context = {
        'title': 'Data Kuari',
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
    }

    return render(request, 'mineral/data/detail.html', context)


# process statistic views
@user_is_manager()
def process_statistic_edit(request, pk):
    data = get_object_or_404(ProcessData, pk=pk)
    statistic_list = ProcessStatistic.objects.filter(data=data)
    next_link = reverse('mineral:process_submission_edit',
                        kwargs={'pk': data.pk})

    context = {
        'title': 'Perangkaan Bulanan kilang pemprosesan mineral',
        'data': data,
        'statistic_list': statistic_list,
        'next_link': next_link,
    }

    return render(request, 'mineral/data/process_statistic/list.html', context=context)


class ProcessStatisticCreateView(UserIsManagerMixin, CreateView):
    template_name = 'mineral/data/process_statistic/form.html'
    form_class = ProcessStatisticForm
    model = ProcessStatistic

    def form_valid(self, form):
        self.data = get_object_or_404(
            ProcessData, pk=self.kwargs['pk'])
        form.instance.data = self.data
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mineral:process_statistic_edit', kwargs={'pk': self.data.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Tambah Perangkaan Bulanan kilang pemprosesan mineral'
        return context


class ProcessStatisticUpdateView(UserIsManagerMixin, UpdateView):
    template_name = 'mineral/data/process_statistic/form.html'
    form_class = ProcessStatisticForm
    model = ProcessStatistic

    def get_success_url(self):
        return reverse('mineral:process_statistic_edit', kwargs={'pk': self.object.data.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Perangkaan Bulanan kilang pemprosesan mineral'
        return context


@user_is_manager()
def process_statistic_delete(request, pk):
    statistic = get_object_or_404(ProcessStatistic, pk=pk)
    if request.method == 'POST':
        statistic.delete()
    return redirect('mineral:process_statistic_edit', pk=statistic.data.pk)


def process_statistic_detail(request, pk):
    statistic = get_object_or_404(ProcessStatistic, pk=pk)
    next_link = reverse("mineral:data_detail", kwargs={
                        "pk": statistic.data.pk})

    context = {
        'title': 'Perangkaan Bulanan kilang pemprosesan mineral',
        'next_link': next_link,
        'statistic': statistic,
    }

    return render(request, 'mineral/data/process_statistic/detail.html', context)


# process submission views
@user_is_manager()
def process_submission_edit(request, pk):
    data = get_object_or_404(ProcessData, pk=pk)
    process_submission_list = ProcessSubmission.objects.filter(data=data)
    next_link = reverse('mineral:local_worker_edit', kwargs={'pk': data.pk})
    prev_link = reverse('mineral:process_statistic_edit',
                        kwargs={'pk': data.pk})

    context = {
        'title': 'Penyerahan/Jualan',
        'data': data,
        'process_submission_list': process_submission_list,
        'next_link': next_link,
        'prev_link': prev_link,
    }

    return render(request, 'mineral/data/process_submission/list.html', context=context)


class ProcessSubmissionCreateView(UserIsManagerMixin, CreateView):
    template_name = 'mineral/data/process_submission/form.html'
    form_class = ProcessSubmissionForm
    model = ProcessSubmission

    def form_valid(self, form):
        self.data = get_object_or_404(
            ProcessData, pk=self.kwargs['pk'])
        form.instance.data = self.data
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mineral:process_submission_edit', kwargs={'pk': self.data.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Tambah Penyerahan/Jualan'
        return context


class ProcessSubmissionUpdateView(UserIsManagerMixin, UpdateView):
    template_name = 'mineral/data/process_submission/form.html'
    form_class = ProcessSubmissionForm
    model = ProcessSubmission

    def get_success_url(self):
        return reverse('mineral:process_submission_edit', kwargs={'pk': self.object.data.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Penyerahan/Jualan'
        return context


@user_is_manager()
def process_submission_delete(request, pk):
    process_submission = get_object_or_404(ProcessSubmission, pk=pk)
    if request.method == 'POST':
        process_submission.delete()
    return redirect('mineral:process_submission_edit', pk=process_submission.data.pk)


def process_submission_detail(request, pk):
    process_submission = get_object_or_404(ProcessSubmission, pk=pk)
    next_link = reverse("mineral:data_detail", kwargs={
                        "pk": process_submission.data.pk})

    context = {
        'title': 'Penyerahan/Jualan',
        'next_link': next_link,
        'process_submission': process_submission,
    }

    return render(request, 'mineral/data/process_submission/detail.html', context)


# local worker views
@user_is_manager()
def local_worker_edit(request, pk):
    data = get_object_or_404(ProcessData, pk=pk)
    prev_link = reverse('mineral:process_submission_edit',
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
            return redirect('mineral:foreign_worker_edit', pk=data.pk)

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

    return render(request, 'mineral/data/worker/form.html', context=context)


# foreign worker views
@user_is_manager()
def foreign_worker_edit(request, pk):
    data = get_object_or_404(ProcessData, pk=pk)
    prev_link = reverse('mineral:local_worker_edit',
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
            return redirect('mineral:machinery_edit', pk=data.pk)

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

    return render(request, 'mineral/data/worker/form.html', context=context)


# machinery views
@user_is_manager()
def machinery_edit(request, pk):
    data = get_object_or_404(ProcessData, pk=pk)
    prev_link = reverse('mineral:foreign_worker_edit',
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
            return redirect('mineral:energy_supply_edit', pk=data.pk)

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

    return render(request, 'mineral/data/machinery/form.html', context=context)


# energy supply views
@user_is_manager()
def energy_supply_edit(request, pk):
    data = get_object_or_404(ProcessData, pk=pk)
    prev_link = reverse('mineral:machinery_edit',
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
            return redirect('mineral:operating_record_edit', pk=data.pk)

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

    return render(request, 'mineral/data/energy_supply/form.html', context=context)


# operating record views
@user_is_manager()
def operating_record_edit(request, pk):
    data = get_object_or_404(ProcessData, pk=pk)
    prev_link = reverse('mineral:energy_supply_edit',
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
            return redirect('mineral:other_edit', pk=data.pk)

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

    return render(request, 'mineral/data/operating_record/form.html', context=context)


# other views
@user_is_manager()
def other_edit(request, pk):
    data = get_object_or_404(ProcessData, pk=pk)
    prev_link = reverse('mineral:operating_record_edit',
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

            return redirect('mineral:data_summary', data.pk)

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

    return render(request, 'mineral/data/other/form.html', context=context)


# summary views
@user_is_manager()
def data_summary(request, pk):
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

    prev_link = reverse('mineral:other_edit',
                        kwargs={"pk": data.pk})

    if request.method == 'POST':
        data_approval = Approval.objects.create(
            data=data, requestor=request.user)

        # noted here
        # jmg_states = User.objects.filter(
        #     groups__name='JMG State', profile__state=data.state)

        # notify = Notify()
        # notify_message = f'{request.user} telah menghantar permohonan data untuk mineral "{data.factory}"'
        # notify_link = reverse('mineral:state:data_list')

        # for jmg_state in jmg_states:
        #     notify.make_notify(jmg_state, notify_message, notify_link)

        return redirect('mineral:data_list')

    context = {
        'title': 'Data PBKPM',
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
        'prev_link': prev_link,
    }

    return render(request, 'mineral/data/summary.html', context)


# comment
def get_comment_data(request, pk):
    data = get_object_or_404(ProcessData, pk=pk)
    data_approval = data.get_last_approval()
    if data_approval.admin_comment:
        return HttpResponse(data_approval.admin_comment)
    elif data_approval.state_comment:
        return HttpResponse(data_approval.state_comment)
    else:
        return HttpResponse('')


# comment views
# def get_comment_data(request, pk):
#     data = get_object_or_404(ProcessData, pk=pk)
#     data_approval = data.get_last_approval()
#     if data_approval.admin_comment:
#         return HttpResponse(data_approval.admin_comment)
#     elif data_approval.state_comment:
#         return HttpResponse(data_approval.state_comment)
#     else:
#         return HttpResponse('')
