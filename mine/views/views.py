from django.http import Http404, HttpResponse
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
    MineDataApproval,
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
    MineReadOnlyForm,
    StatisticReadOnlyForm,
    LocalOperatorReadOnlyForm,
    LocalContractorReadOnlyForm,
    ForeignOperatorReadOnlyForm,
    ForeignContractorReadOnlyForm,
    InternalCombustionMachineryReadOnlyForm,
    ElectricMachineryReadOnlyForm,
    EnergySupplyReadOnlyForm,
    OperatingRecordReadOnlyForm,
)


class MineListView(ListView):
    template_name = 'mine/list.html'
    model = Mine
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Senarai Lombong'
        return context


# class MineStateListView(ListView):
#     template_name = 'mine/list_jmg.html'
#     model = Mine
#     paginate_by = 10
#     ordering = ['-created_at']

#     def get_queryset(self):
#         queryset = super().get_queryset().filter(
#             user__profile__state=self.request.user.profile.state)
#         id_list = []
#         for mine in queryset:
#             approval = mine.get_last_approval()
#             if approval:
#                 if approval.state_approved == None:
#                     id_list.append(mine.id)
#         queryset = queryset.filter(id__in=id_list)
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = 'Senarai Kuari'
#         return context


# class MineStateAdminListView(ListView):
#     template_name = 'mine/list_jmg.html'
#     model = Mine
#     paginate_by = 10
#     ordering = ['-created_at']

#     def get_queryset(self):
#         queryset = super().get_queryset().filter(
#             user__profile__state=self.request.user.profile.state)
#         id_list = []
#         for mine in queryset:
#             approval = mine.get_last_approval()
#             if approval:
#                 if approval.state_approved == True and approval.admin_approved == None:
#                     id_list.append(mine.id)
#         queryset = queryset.filter(id__in=id_list)
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = 'Senarai Kuari'
#         return context


# class MineHQListView(ListView):
#     template_name = 'mine/list_jmg.html'
#     model = Mine
#     paginate_by = 10
#     ordering = ['-created_at']

#     def get_queryset(self):
#         queryset = super().get_queryset().filter(
#             user__profile__state=self.request.user.profile.state)
#         id_list = []
#         for mine in queryset:
#             approval = mine.get_last_approval()
#             if approval:
#                 if approval.state_approved == True and approval.admin_approved == True:
#                     id_list.append(mine.id)
#         queryset = queryset.filter(id__in=id_list)
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = 'Senarai Kuari'
#         return context


# class MineListsView(ListView):
#     template_name = 'mine/listmine.html'
#     model = Mine
#     paginate_by = 10
#     ordering = ['-created_at']

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = 'Senarai Lombong'
#         return context


# class MineCreateView(CreateView):
#     template_name = 'mine/form.html'
#     model = Mine
#     form_class = MineForm
#     success_url = reverse_lazy('mine:list')

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = 'RPLB Ringkasan Perangkaan Lombong Bulan'
#         return context


# class MineUpdateView(UpdateView):
#     template_name = 'mine/form.html'
#     model = Mine
#     form_class = MineForm
#     success_url = reverse_lazy('mine:list')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = 'RPLB Ringkasan Perangkaan Lombong Bulan (update)'
#         return context


# def statistic_edit(request, pk):
#     mine = get_object_or_404(Mine, pk=pk)
#     try:
#         statistic = Statistic.objects.get(mine=mine)
#     except Statistic.DoesNotExist:
#         statistic = None

#     if request.method == 'POST':
#         if statistic == None:
#             form = StatisticForm(request.POST)
#         else:
#             form = StatisticForm(
#                 request.POST, instance=statistic)

#         if form.is_valid():
#             form.instance.mine = mine
#             form.save()
#             return redirect('mine:local_worker_edit', pk=mine.pk)

#     else:
#         if statistic == None:
#             form = StatisticForm()
#         else:
#             form = StatisticForm(instance=statistic)

#     context = {
#         'title': 'Edit Perangkaan',
#         'form': form,
#     }

#     return render(request, 'mine/statistic/form.html', context=context)


# def local_worker_edit(request, pk):
#     mine = get_object_or_404(Mine, pk=pk)
#     prev_link = reverse('mine:statistic_edit',
#                         kwargs={"pk": mine.pk})
#     try:
#         local_operator = LocalOperator.objects.get(mine=mine)
#         local_contractor = LocalContractor.objects.get(mine=mine)
#     except LocalOperator.DoesNotExist:
#         local_operator = None
#         local_contractor = None

#     if request.method == 'POST':
#         if local_operator == None:
#             operator_form = LocalOperatorForm(request.POST)
#             contractor_form = LocalContractorForm(
#                 request.POST, prefix='second')
#         else:
#             operator_form = LocalOperatorForm(
#                 request.POST, instance=local_operator)
#             contractor_form = LocalContractorForm(
#                 request.POST, instance=local_contractor, prefix='second')

#         if operator_form.is_valid() and contractor_form.is_valid():
#             operator_form.instance.mine = mine
#             contractor_form.instance.mine = mine
#             operator_form.save()
#             contractor_form.save()
#             return redirect('mine:foreign_worker_edit', pk=mine.pk)

#     else:
#         if local_operator == None:
#             operator_form = LocalOperatorForm()
#             contractor_form = LocalContractorForm(prefix='second')
#         else:
#             operator_form = LocalOperatorForm(instance=local_operator)
#             contractor_form = LocalContractorForm(
#                 instance=local_contractor, prefix='second')

#     context = {
#         'title': 'Edit Pekerjaan (Tempatan)',
#         'operator_form': operator_form,
#         'contractor_form': contractor_form,
#         'prev_link': prev_link,
#     }

#     return render(request, 'mine/worker/form.html', context=context)


# def foreign_worker_edit(request, pk):
#     mine = get_object_or_404(Mine, pk=pk)
#     prev_link = reverse('mine:local_worker_edit',
#                         kwargs={"pk": mine.pk})
#     try:
#         foreign_operator = ForeignOperator.objects.get(mine=mine)
#         foreign_contractor = ForeignContractor.objects.get(mine=mine)
#     except ForeignOperator.DoesNotExist:
#         foreign_operator = None
#         foreign_contractor = None

#     if request.method == 'POST':
#         if foreign_operator == None:
#             operator_form = ForeignOperatorForm(request.POST)
#             contractor_form = ForeignContractorForm(
#                 request.POST, prefix='second')
#         else:
#             operator_form = ForeignOperatorForm(
#                 request.POST, instance=foreign_operator)
#             contractor_form = ForeignContractorForm(
#                 request.POST, instance=foreign_contractor, prefix='second')

#         if operator_form.is_valid() and contractor_form.is_valid():
#             operator_form.instance.mine = mine
#             contractor_form.instance.mine = mine
#             operator_form.save()
#             contractor_form.save()
#             return redirect('mine:machinery_edit', pk=mine.pk)

#     else:
#         if foreign_operator == None:
#             operator_form = ForeignOperatorForm()
#             contractor_form = ForeignContractorForm(prefix='second')
#         else:
#             operator_form = ForeignOperatorForm(instance=foreign_operator)
#             contractor_form = ForeignContractorForm(
#                 instance=foreign_contractor, prefix='second')

#     context = {
#         'title': 'Edit Pekerjaan (Asing)',
#         'operator_form': operator_form,
#         'contractor_form': contractor_form,
#         'prev_link': prev_link,
#     }

#     return render(request, 'mine/worker/form.html', context=context)


# def machinery_edit(request, pk):
#     mine = get_object_or_404(Mine, pk=pk)
#     prev_link = reverse('mine:foreign_worker_edit',
#                         kwargs={"pk": mine.pk})
#     try:
#         combustion_machinery = InternalCombustionMachinery.objects.get(
#             mine=mine)
#         electric_machinery = ElectricMachinery.objects.get(mine=mine)
#     except InternalCombustionMachinery.DoesNotExist:
#         combustion_machinery = None
#         electric_machinery = None

#     if request.method == 'POST':
#         if combustion_machinery == None:
#             combustion_form = InternalCombustionMachineryForm(request.POST)
#             electric_form = ElectricMachineryForm(
#                 request.POST, prefix='second')
#         else:
#             combustion_form = InternalCombustionMachineryForm(
#                 request.POST, instance=combustion_machinery)
#             electric_form = ElectricMachineryForm(
#                 request.POST, instance=electric_machinery, prefix='second')

#         if combustion_form.is_valid() and electric_form.is_valid():
#             combustion_form.instance.mine = mine
#             electric_form.instance.mine = mine
#             combustion_form.save()
#             electric_form.save()
#             return redirect('mine:energy_supply_edit', pk=mine.pk)

#     else:
#         if combustion_machinery == None:
#             combustion_form = InternalCombustionMachineryForm()
#             electric_form = ElectricMachineryForm(prefix='second')
#         else:
#             combustion_form = InternalCombustionMachineryForm(
#                 instance=combustion_machinery)
#             electric_form = ElectricMachineryForm(
#                 instance=electric_machinery, prefix='second')

#     context = {
#         'title': 'Edit Jentera',
#         'combustion_form': combustion_form,
#         'electric_form': electric_form,
#         'prev_link': prev_link,
#     }

#     return render(request, 'mine/machinery/form.html', context=context)


# def energy_supply_edit(request, pk):
#     mine = get_object_or_404(Mine, pk=pk)
#     prev_link = reverse('mine:machinery_edit',
#                         kwargs={"pk": mine.pk})
#     try:
#         energy_supply = EnergySupply.objects.get(mine=mine)
#     except EnergySupply.DoesNotExist:
#         energy_supply = None

#     if request.method == 'POST':
#         if energy_supply == None:
#             form = EnergySupplyForm(request.POST)
#         else:
#             form = EnergySupplyForm(
#                 request.POST, instance=energy_supply)

#         if form.is_valid():
#             form.instance.mine = mine
#             form.save()
#             return redirect('mine:operating_record_edit', pk=mine.pk)

#     else:
#         if energy_supply == None:
#             form = EnergySupplyForm()
#         else:
#             form = EnergySupplyForm(instance=energy_supply)

#     context = {
#         'title': 'Edit Bahan Tenaga',
#         'form': form,
#         'prev_link': prev_link,
#     }

#     return render(request, 'mine/energy_supply/form.html', context=context)


# def operating_record_edit(request, pk):
#     mine = get_object_or_404(Mine, pk=pk)
#     prev_link = reverse('mine:energy_supply_edit',
#                         kwargs={"pk": mine.pk})
#     try:
#         operating_record = OperatingRecord.objects.get(mine=mine)
#     except OperatingRecord.DoesNotExist:
#         operating_record = None

#     if request.method == 'POST':
#         if operating_record == None:
#             form = OperatingRecordForm(request.POST)
#         else:
#             form = OperatingRecordForm(
#                 request.POST, instance=operating_record)

#         if form.is_valid():
#             form.instance.mine = mine
#             form.save()
#             return redirect('mine:list')

#     else:
#         if operating_record == None:
#             form = OperatingRecordForm()
#         else:
#             form = OperatingRecordForm(instance=operating_record)

#     context = {
#         'title': 'Edit Rekod Operasi',
#         'form': form,
#         'prev_link': prev_link,
#     }

#     return render(request, 'mine/operating_record/form.html', context=context)


# def mine_readonly(request, pk):
#     mine = get_object_or_404(Mine, pk=pk)
#     next_link = reverse('mine:statistic_readonly',
#                         kwargs={"pk": mine.pk})
#     form = MineReadOnlyForm(instance=mine)

#     context = {
#         'title': 'Data Lombong',
#         'form': form,
#         'next_link': next_link,
#     }

#     return render(request, 'mine/readonly.html', context=context)


# def statistic_readonly(request, pk):
#     mine = get_object_or_404(Mine, pk=pk)
#     prev_link = reverse('mine:readonly',
#                         kwargs={"pk": mine.pk})
#     next_link = reverse('mine:local_worker_readonly',
#                         kwargs={"pk": mine.pk})
#     statistic = get_object_or_404(Statistic, mine=mine)
#     form = StatisticReadOnlyForm(instance=statistic)

#     context = {
#         'title': 'Perangkaan',
#         'form': form,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'mine/statistic/readonly.html', context=context)


# def local_worker_readonly(request, pk):
#     mine = get_object_or_404(Mine, pk=pk)
#     prev_link = reverse('mine:statistic_readonly',
#                         kwargs={"pk": mine.pk})
#     next_link = reverse('mine:foreign_worker_readonly',
#                         kwargs={"pk": mine.pk})
#     local_operator = get_object_or_404(LocalOperator, mine=mine)
#     local_contractor = get_object_or_404(LocalContractor, mine=mine)
#     operator_form = LocalOperatorReadOnlyForm(instance=local_operator)
#     contractor_form = LocalContractorReadOnlyForm(
#         instance=local_contractor, prefix='second')

#     context = {
#         'title': 'Pekerjaan (Tempatan)',
#         'operator_form': operator_form,
#         'contractor_form': contractor_form,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'mine/worker/readonly.html', context=context)


# def foreign_worker_readonly(request, pk):
#     mine = get_object_or_404(Mine, pk=pk)
#     prev_link = reverse('mine:local_worker_readonly',
#                         kwargs={"pk": mine.pk})
#     next_link = reverse('mine:machinery_readonly',
#                         kwargs={"pk": mine.pk})
#     foreign_operator = get_object_or_404(ForeignOperator, mine=mine)
#     foreign_contractor = get_object_or_404(ForeignContractor, mine=mine)
#     operator_form = ForeignOperatorReadOnlyForm(instance=foreign_operator)
#     contractor_form = ForeignContractorReadOnlyForm(
#         instance=foreign_contractor, prefix='second')

#     context = {
#         'title': 'Pekerjaan (Asing)',
#         'operator_form': operator_form,
#         'contractor_form': contractor_form,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'mine/worker/readonly.html', context=context)


# def machinery_readonly(request, pk):
#     mine = get_object_or_404(Mine, pk=pk)
#     prev_link = reverse('mine:foreign_worker_readonly',
#                         kwargs={"pk": mine.pk})
#     next_link = reverse('mine:energy_supply_readonly',
#                         kwargs={"pk": mine.pk})
#     combustion_machinery = get_object_or_404(
#         InternalCombustionMachinery, mine=mine)
#     electric_machinery = get_object_or_404(ElectricMachinery, mine=mine)
#     combustion_form = InternalCombustionMachineryReadOnlyForm(
#         instance=combustion_machinery)
#     electric_form = ElectricMachineryReadOnlyForm(
#         instance=electric_machinery, prefix='second')

#     context = {
#         'title': 'Jentera',
#         'combustion_form': combustion_form,
#         'electric_form': electric_form,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'mine/machinery/readonly.html', context=context)


# def energy_supply_readonly(request, pk):
#     mine = get_object_or_404(Mine, pk=pk)
#     prev_link = reverse('mine:machinery_readonly',
#                         kwargs={"pk": mine.pk})
#     next_link = reverse('mine:operating_record_readonly',
#                         kwargs={"pk": mine.pk})
#     energy_supply = get_object_or_404(EnergySupply, mine=mine)
#     form = EnergySupplyReadOnlyForm(instance=energy_supply)

#     context = {
#         'title': 'Bahan Tenaga',
#         'form': form,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'mine/energy_supply/readonly.html', context=context)


# def operating_record_readonly(request, pk):
#     mine = get_object_or_404(Mine, pk=pk)
#     prev_link = reverse('mine:energy_supply_readonly',
#                         kwargs={"pk": mine.pk})
#     operating_record = get_object_or_404(OperatingRecord, mine=mine)
#     form = OperatingRecordReadOnlyForm(instance=operating_record)

#     context = {
#         'title': 'Rekod Operasi',
#         'form': form,
#         'prev_link': prev_link,
#         'mine_id': mine.id,
#     }

#     return render(request, 'mine/operating_record/readonly.html', context=context)


# def submit_mine(request, pk):
#     if request.method == 'POST':
#         mine = get_object_or_404(Mine, pk=pk)
#         mine_approval = MineApproval.objects.create(
#             mine=mine, requestor=request.user)
#         return redirect('mine:list')

#     else:
#         raise Http404


# def state_approve_mine(request, pk):
#     if request.method == 'POST':
#         mine = get_object_or_404(Mine, pk=pk)
#         mine_approval = mine.get_last_approval()
#         mine_approval.state_inspector = request.user
#         mine_approval.state_approved = True
#         mine_approval.save()
#         return redirect('mine:list_state')

#     else:
#         raise Http404


# def state_reject_mine(request, pk):
#     if request.method == 'POST':
#         mine = get_object_or_404(Mine, pk=pk)
#         mine_approval = mine.get_last_approval()
#         mine_approval.state_inspector = request.user
#         mine_approval.state_comment = request.POST.get('comment')
#         mine_approval.state_approved = False
#         mine_approval.save()
#         return redirect('mine:list_state')

#     else:
#         raise Http404


# def state_admin_approve_mine(request, pk):
#     if request.method == 'POST':
#         mine = get_object_or_404(Mine, pk=pk)
#         mine_approval = mine.get_last_approval()
#         mine_approval.admin_inspector = request.user
#         mine_approval.admin_approved = True
#         mine_approval.save()
#         return redirect('mine:list_state_admin')

#     else:
#         raise Http404


# def state_admin_reject_mine(request, pk):
#     if request.method == 'POST':
#         mine = get_object_or_404(Mine, pk=pk)
#         mine_approval = mine.get_last_approval()
#         mine_approval.admin_inspector = request.user
#         mine_approval.admin_comment = request.POST.get('comment')
#         mine_approval.admin_approved = False
#         mine_approval.save()
#         return redirect('mine:list_state_admin')

#     else:
#         raise Http404


# def get_comment_mine(request, pk):
#     mine = get_object_or_404(Mine, pk=pk)
#     mine_approval = mine.get_last_approval()
#     if mine_approval.admin_comment:
#         return HttpResponse(mine_approval.admin_comment)
#     elif mine_approval.state_comment:
#         return HttpResponse(mine_approval.state_comment)
#     else:
#         return HttpResponse('')
