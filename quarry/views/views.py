from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView

from ..models import (
    Quarry,
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
    QuarryForm,
    QuarryMinerForm,
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
from ..forms.readonly import (
    QuarryReadOnlyForm,
    QuarryMinerReadOnlyForm,
    QuarryMinerDataReadOnlyForm,
    ProductionStatisticReadOnlyForm,
    SalesSubmissionReadOnlyForm,
    LocalFinalUsesReadOnlyForm,
    ExportFinalUsesReadOnlyForm,
    LocalOperatorReadOnlyForm,
    LocalContractorReadOnlyForm,
    ForeignOperatorReadOnlyForm,
    ForeignContractorReadOnlyForm,
    InternalCombustionMachineryReadOnlyForm,
    ElectricMachineryReadOnlyForm,
    DailyExplosiveReadOnlyForm,
    EnergySupplyReadOnlyForm,
    OperatingRecordReadOnlyForm,
    RoyaltiesReadOnlyForm,
    OtherReadOnlyForm,
)


class QuarryListView(ListView):
    template_name = 'quarry/list.html'
    model = Quarry
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Senarai Kuari'
        return context


# class QuarryStateListView(ListView):
#     template_name = 'quarry/list_jmg.html'
#     model = Quarry
#     paginate_by = 10
#     ordering = ['-created_at']

#     def get_queryset(self):
#         queryset = super().get_queryset().filter(
#             user__profile__state=self.request.user.profile.state)
#         id_list = []
#         for quarry in queryset:
#             approval = quarry.get_last_approval()
#             if approval:
#                 if approval.state_approved == None:
#                     id_list.append(quarry.id)
#         queryset = queryset.filter(id__in=id_list)
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = 'Senarai Kuari'
#         return context


# class QuarryStateAdminListView(ListView):
#     template_name = 'quarry/list_jmg.html'
#     model = Quarry
#     paginate_by = 10
#     ordering = ['-created_at']

#     def get_queryset(self):
#         queryset = super().get_queryset().filter(
#             user__profile__state=self.request.user.profile.state)
#         id_list = []
#         for quarry in queryset:
#             approval = quarry.get_last_approval()
#             if approval:
#                 if approval.state_approved == True and approval.admin_approved == None:
#                     id_list.append(quarry.id)
#         queryset = queryset.filter(id__in=id_list)
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = 'Senarai Kuari'
#         return context


# class QuarryHQListView(ListView):
#     template_name = 'quarry/list_jmg.html'
#     model = Quarry
#     paginate_by = 10
#     ordering = ['-created_at']

#     def get_queryset(self):
#         queryset = super().get_queryset().filter(
#             user__profile__state=self.request.user.profile.state)
#         id_list = []
#         for quarry in queryset:
#             approval = quarry.get_last_approval()
#             if approval:
#                 if approval.state_approved == True and approval.admin_approved == True:
#                     id_list.append(quarry.id)
#         queryset = queryset.filter(id__in=id_list)
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = 'Senarai Kuari'
#         return context


# class QuarryListsView(ListView):
#     template_name = 'quarry/listquarry.html'
#     model = Quarry
#     paginate_by = 10
#     ordering = ['-created_at']

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = 'Senarai Kuari'
#         return context


# class QuarryCreateView(CreateView):
#     template_name = 'quarry/form.html'
#     model = Quarry
#     form_class = QuarryForm
#     success_url = reverse_lazy('quarry:list')

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = 'Tambah Kuari Baru'
#         return context


# class QuarryUpdateView(UpdateView):
#     template_name = 'quarry/form.html'
#     model = Quarry
#     form_class = QuarryForm
#     success_url = reverse_lazy('quarry:list')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = 'Kemaskini Data Kuari'
#         return context


# def production_statistic_edit(request, pk):
#     quarry = get_object_or_404(Quarry, pk=pk)
#     try:
#         production_statistic = ProductionStatistic.objects.get(quarry=quarry)
#     except ProductionStatistic.DoesNotExist:
#         production_statistic = None

#     if request.method == 'POST':
#         if production_statistic == None:
#             form = ProductionStatisticForm(request.POST)
#         else:
#             form = ProductionStatisticForm(
#                 request.POST, instance=production_statistic)

#         if form.is_valid():
#             form.instance.quarry = quarry
#             form.save()
#             return redirect('quarry:sales_submission_edit', pk=quarry.pk)

#     else:
#         if production_statistic == None:
#             form = ProductionStatisticForm()
#         else:
#             form = ProductionStatisticForm(instance=production_statistic)

#     context = {
#         'title': 'Edit Perangkaan Pengeluaran',
#         'form': form,
#     }

#     return render(request, 'quarry/production_statistic/form.html', context=context)


# def sales_submission_edit(request, pk):
#     quarry = get_object_or_404(Quarry, pk=pk)
#     prev_link = reverse('quarry:production_statistic_edit',
#                         kwargs={"pk": quarry.pk})
#     try:
#         sales_submission = SalesSubmission.objects.get(quarry=quarry)
#     except SalesSubmission.DoesNotExist:
#         sales_submission = None

#     if request.method == 'POST':
#         if sales_submission == None:
#             form = SalesSubmissionForm(request.POST)
#         else:
#             form = SalesSubmissionForm(
#                 request.POST, instance=sales_submission)

#         if form.is_valid():
#             form.instance.quarry = quarry
#             form.save()
#             return redirect('quarry:final_uses_edit', pk=quarry.pk)

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

#     return render(request, 'quarry/sales_submission/form.html', context=context)


# def final_uses_edit(request, pk):
#     quarry = get_object_or_404(Quarry, pk=pk)
#     prev_link = reverse('quarry:sales_submission_edit',
#                         kwargs={"pk": quarry.pk})
#     try:
#         local_final_uses = LocalFinalUses.objects.get(quarry=quarry)
#         export_final_uses = ExportFinalUses.objects.get(quarry=quarry)
#     except LocalFinalUses.DoesNotExist:
#         local_final_uses = None
#         export_final_uses = None

#     if request.method == 'POST':
#         if local_final_uses == None:
#             local_form = LocalFinalUsesForm(request.POST)
#             export_form = ExportFinalUsesForm(request.POST, prefix='second')
#         else:
#             local_form = LocalFinalUsesForm(
#                 request.POST, instance=local_final_uses)
#             export_form = ExportFinalUsesForm(
#                 request.POST, instance=export_final_uses, prefix='second')

#         if local_form.is_valid() and export_form.is_valid():
#             local_form.instance.quarry = quarry
#             export_form.instance.quarry = quarry
#             local_form.save()
#             export_form.save()
#             return redirect('quarry:local_worker_edit', pk=quarry.pk)

#     else:
#         if local_final_uses == None:
#             local_form = LocalFinalUsesForm()
#             export_form = ExportFinalUsesForm(prefix='second')
#         else:
#             local_form = LocalFinalUsesForm(instance=local_final_uses)
#             export_form = ExportFinalUsesForm(
#                 instance=export_final_uses, prefix='second')

#     context = {
#         'title': 'Edit Kegunaan Akhir',
#         'local_form': local_form,
#         'export_form': export_form,
#         'prev_link': prev_link,
#     }

#     return render(request, 'quarry/final_uses/form.html', context=context)


# def local_worker_edit(request, pk):
#     quarry = get_object_or_404(Quarry, pk=pk)
#     prev_link = reverse('quarry:final_uses_edit',
#                         kwargs={"pk": quarry.pk})
#     try:
#         local_operator = LocalOperator.objects.get(quarry=quarry)
#         local_contractor = LocalContractor.objects.get(quarry=quarry)
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
#             operator_form.instance.quarry = quarry
#             contractor_form.instance.quarry = quarry
#             operator_form.save()
#             contractor_form.save()
#             return redirect('quarry:foreign_worker_edit', pk=quarry.pk)

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

#     return render(request, 'quarry/worker/form.html', context=context)


# def foreign_worker_edit(request, pk):
#     quarry = get_object_or_404(Quarry, pk=pk)
#     prev_link = reverse('quarry:local_worker_edit',
#                         kwargs={"pk": quarry.pk})
#     try:
#         foreign_operator = ForeignOperator.objects.get(quarry=quarry)
#         foreign_contractor = ForeignContractor.objects.get(quarry=quarry)
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
#             operator_form.instance.quarry = quarry
#             contractor_form.instance.quarry = quarry
#             operator_form.save()
#             contractor_form.save()
#             return redirect('quarry:machinery_edit', pk=quarry.pk)

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

#     return render(request, 'quarry/worker/form.html', context=context)


# def machinery_edit(request, pk):
#     quarry = get_object_or_404(Quarry, pk=pk)
#     prev_link = reverse('quarry:foreign_worker_edit',
#                         kwargs={"pk": quarry.pk})
#     try:
#         combustion_machinery = InternalCombustionMachinery.objects.get(
#             quarry=quarry)
#         electric_machinery = ElectricMachinery.objects.get(quarry=quarry)
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
#             combustion_form.instance.quarry = quarry
#             electric_form.instance.quarry = quarry
#             combustion_form.save()
#             electric_form.save()
#             return redirect('quarry:daily_explosive_edit', pk=quarry.pk)

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

#     return render(request, 'quarry/machinery/form.html', context=context)


# def daily_explosive_edit(request, pk):
#     quarry = get_object_or_404(Quarry, pk=pk)
#     prev_link = reverse('quarry:machinery_edit',
#                         kwargs={"pk": quarry.pk})
#     try:
#         daily_explosive = DailyExplosive.objects.get(quarry=quarry)
#     except DailyExplosive.DoesNotExist:
#         daily_explosive = None

#     if request.method == 'POST':
#         if daily_explosive == None:
#             form = DailyExplosiveForm(request.POST)
#         else:
#             form = DailyExplosiveForm(
#                 request.POST, instance=daily_explosive)

#         if form.is_valid():
#             form.instance.quarry = quarry
#             form.save()
#             return redirect('quarry:energy_supply_edit', pk=quarry.pk)

#     else:
#         if daily_explosive == None:
#             form = DailyExplosiveForm()
#         else:
#             form = DailyExplosiveForm(instance=daily_explosive)

#     context = {
#         'title': 'Edit Bahan Letupan Harian',
#         'form': form,
#         'prev_link': prev_link,
#     }

#     return render(request, 'quarry/daily_explosive/form.html', context=context)


# def energy_supply_edit(request, pk):
#     quarry = get_object_or_404(Quarry, pk=pk)
#     prev_link = reverse('quarry:daily_explosive_edit',
#                         kwargs={"pk": quarry.pk})
#     try:
#         energy_supply = EnergySupply.objects.get(quarry=quarry)
#     except EnergySupply.DoesNotExist:
#         energy_supply = None

#     if request.method == 'POST':
#         if energy_supply == None:
#             form = EnergySupplyForm(request.POST)
#         else:
#             form = EnergySupplyForm(
#                 request.POST, instance=energy_supply)

#         if form.is_valid():
#             form.instance.quarry = quarry
#             form.save()
#             return redirect('quarry:operating_record_edit', pk=quarry.pk)

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

#     return render(request, 'quarry/energy_supply/form.html', context=context)


# def operating_record_edit(request, pk):
#     quarry = get_object_or_404(Quarry, pk=pk)
#     prev_link = reverse('quarry:energy_supply_edit',
#                         kwargs={"pk": quarry.pk})
#     try:
#         operating_record = OperatingRecord.objects.get(quarry=quarry)
#     except OperatingRecord.DoesNotExist:
#         operating_record = None

#     if request.method == 'POST':
#         if operating_record == None:
#             form = OperatingRecordForm(request.POST)
#         else:
#             form = OperatingRecordForm(
#                 request.POST, instance=operating_record)

#         if form.is_valid():
#             form.instance.quarry = quarry
#             form.save()
#             return redirect('quarry:royalties_edit', pk=quarry.pk)

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

#     return render(request, 'quarry/operating_record/form.html', context=context)


# def royalties_edit(request, pk):
#     quarry = get_object_or_404(Quarry, pk=pk)
#     prev_link = reverse('quarry:operating_record_edit',
#                         kwargs={"pk": quarry.pk})
#     try:
#         royalties = Royalties.objects.get(quarry=quarry)
#     except Royalties.DoesNotExist:
#         royalties = None

#     if request.method == 'POST':
#         if royalties == None:
#             form = RoyaltiesForm(request.POST)
#         else:
#             form = RoyaltiesForm(
#                 request.POST, instance=royalties)

#         if form.is_valid():
#             form.instance.quarry = quarry
#             form.save()
#             return redirect('quarry:other_edit', pk=quarry.pk)

#     else:
#         if royalties == None:
#             form = RoyaltiesForm()
#         else:
#             form = RoyaltiesForm(instance=royalties)

#     context = {
#         'title': 'Edit Royalti',
#         'form': form,
#         'prev_link': prev_link,
#     }

#     return render(request, 'quarry/royalties/form.html', context=context)


# def other_edit(request, pk):
#     quarry = get_object_or_404(Quarry, pk=pk)
#     prev_link = reverse('quarry:royalties_edit',
#                         kwargs={"pk": quarry.pk})
#     try:
#         other = Other.objects.get(quarry=quarry)
#     except Other.DoesNotExist:
#         other = None

#     if request.method == 'POST':
#         if other == None:
#             form = OtherForm(request.POST)
#         else:
#             form = OtherForm(
#                 request.POST, instance=other)

#         if form.is_valid():
#             form.instance.quarry = quarry
#             form.save()
#             return redirect('quarry:list')

#     else:
#         if other == None:
#             form = OtherForm()
#         else:
#             form = OtherForm(instance=other)

#     context = {
#         'title': 'Edit Lain-lain',
#         'form': form,
#         'prev_link': prev_link,
#     }

#     return render(request, 'quarry/other/form.html', context=context)


# def quarry_readonly(request, pk):
#     quarry = get_object_or_404(Quarry, pk=pk)
#     next_link = reverse('quarry:production_statistic_readonly',
#                         kwargs={"pk": quarry.pk})
#     form = QuarryReadOnlyForm(instance=quarry)

#     context = {
#         'title': 'Data Kuari',
#         'form': form,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/readonly.html', context=context)


# def production_statistic_readonly(request, pk):
#     quarry = get_object_or_404(Quarry, pk=pk)
#     prev_link = reverse('quarry:readonly',
#                         kwargs={"pk": quarry.pk})
#     next_link = reverse('quarry:sales_submission_readonly',
#                         kwargs={"pk": quarry.pk})
#     production_statistic = get_object_or_404(
#         ProductionStatistic, quarry=quarry)
#     form = ProductionStatisticReadOnlyForm(instance=production_statistic)

#     context = {
#         'title': 'Perangkaan Pengeluaran',
#         'form': form,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/production_statistic/readonly.html', context=context)


# def sales_submission_readonly(request, pk):
#     quarry = get_object_or_404(Quarry, pk=pk)
#     prev_link = reverse('quarry:production_statistic_readonly',
#                         kwargs={"pk": quarry.pk})
#     next_link = reverse('quarry:final_uses_readonly',
#                         kwargs={"pk": quarry.pk})
#     sales_submission = get_object_or_404(SalesSubmission, quarry=quarry)
#     form = SalesSubmissionReadOnlyForm(instance=sales_submission)

#     context = {
#         'title': 'Penyerahan Jualan',
#         'form': form,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/sales_submission/readonly.html', context=context)


# def final_uses_readonly(request, pk):
#     quarry = get_object_or_404(Quarry, pk=pk)
#     prev_link = reverse('quarry:sales_submission_readonly',
#                         kwargs={"pk": quarry.pk})
#     next_link = reverse('quarry:local_worker_readonly',
#                         kwargs={"pk": quarry.pk})
#     local_final_uses = get_object_or_404(LocalFinalUses, quarry=quarry)
#     export_final_uses = get_object_or_404(ExportFinalUses, quarry=quarry)
#     local_form = LocalFinalUsesReadOnlyForm(instance=local_final_uses)
#     export_form = ExportFinalUsesReadOnlyForm(
#         instance=export_final_uses, prefix='second')

#     context = {
#         'title': 'Kegunaan Akhir',
#         'local_form': local_form,
#         'export_form': export_form,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/final_uses/readonly.html', context=context)


# def local_worker_readonly(request, pk):
#     quarry = get_object_or_404(Quarry, pk=pk)
#     prev_link = reverse('quarry:final_uses_readonly',
#                         kwargs={"pk": quarry.pk})
#     next_link = reverse('quarry:foreign_worker_readonly',
#                         kwargs={"pk": quarry.pk})
#     local_operator = get_object_or_404(LocalOperator, quarry=quarry)
#     local_contractor = get_object_or_404(LocalContractor, quarry=quarry)
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

#     return render(request, 'quarry/worker/readonly.html', context=context)


# def foreign_worker_readonly(request, pk):
#     quarry = get_object_or_404(Quarry, pk=pk)
#     prev_link = reverse('quarry:local_worker_readonly',
#                         kwargs={"pk": quarry.pk})
#     next_link = reverse('quarry:machinery_readonly',
#                         kwargs={"pk": quarry.pk})
#     foreign_operator = get_object_or_404(ForeignOperator, quarry=quarry)
#     foreign_contractor = get_object_or_404(ForeignContractor, quarry=quarry)
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

#     return render(request, 'quarry/worker/readonly.html', context=context)


# def machinery_readonly(request, pk):
#     quarry = get_object_or_404(Quarry, pk=pk)
#     prev_link = reverse('quarry:foreign_worker_readonly',
#                         kwargs={"pk": quarry.pk})
#     next_link = reverse('quarry:daily_explosive_readonly',
#                         kwargs={"pk": quarry.pk})
#     combustion_machinery = get_object_or_404(
#         InternalCombustionMachinery, quarry=quarry)
#     electric_machinery = get_object_or_404(ElectricMachinery, quarry=quarry)
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

#     return render(request, 'quarry/machinery/readonly.html', context=context)


# def daily_explosive_readonly(request, pk):
#     quarry = get_object_or_404(Quarry, pk=pk)
#     prev_link = reverse('quarry:machinery_readonly',
#                         kwargs={"pk": quarry.pk})
#     next_link = reverse('quarry:energy_supply_readonly',
#                         kwargs={"pk": quarry.pk})
#     daily_explosive = get_object_or_404(DailyExplosive, quarry=quarry)
#     form = DailyExplosiveReadOnlyForm(instance=daily_explosive)

#     context = {
#         'title': 'Bahan Letupan Harian',
#         'form': form,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/daily_explosive/readonly.html', context=context)


# def energy_supply_readonly(request, pk):
#     quarry = get_object_or_404(Quarry, pk=pk)
#     prev_link = reverse('quarry:daily_explosive_readonly',
#                         kwargs={"pk": quarry.pk})
#     next_link = reverse('quarry:operating_record_readonly',
#                         kwargs={"pk": quarry.pk})
#     energy_supply = get_object_or_404(EnergySupply, quarry=quarry)
#     form = EnergySupplyReadOnlyForm(instance=energy_supply)

#     context = {
#         'title': 'Bahan Tenaga',
#         'form': form,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/energy_supply/readonly.html', context=context)


# def operating_record_readonly(request, pk):
#     quarry = get_object_or_404(Quarry, pk=pk)
#     prev_link = reverse('quarry:energy_supply_readonly',
#                         kwargs={"pk": quarry.pk})
#     next_link = reverse('quarry:royalties_readonly',
#                         kwargs={"pk": quarry.pk})
#     operating_record = get_object_or_404(OperatingRecord, quarry=quarry)
#     form = OperatingRecordReadOnlyForm(instance=operating_record)

#     context = {
#         'title': 'Rekod Operasi',
#         'form': form,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/operating_record/readonly.html', context=context)


# def royalties_readonly(request, pk):
#     quarry = get_object_or_404(Quarry, pk=pk)
#     prev_link = reverse('quarry:operating_record_readonly',
#                         kwargs={"pk": quarry.pk})
#     next_link = reverse('quarry:other_readonly',
#                         kwargs={"pk": quarry.pk})
#     royalties = get_object_or_404(Royalties, quarry=quarry)
#     form = RoyaltiesReadOnlyForm(instance=royalties)

#     context = {
#         'title': 'Royalti',
#         'form': form,
#         'prev_link': prev_link,
#         'next_link': next_link,
#     }

#     return render(request, 'quarry/royalties/readonly.html', context=context)


# def other_readonly(request, pk):
#     quarry = get_object_or_404(Quarry, pk=pk)
#     prev_link = reverse('quarry:royalties_readonly',
#                         kwargs={"pk": quarry.pk})
#     other = get_object_or_404(Other, quarry=quarry)
#     form = OtherReadOnlyForm(instance=other)

#     context = {
#         'title': 'Lain-lain',
#         'form': form,
#         'prev_link': prev_link,
#         'quarry_id': quarry.id,
#     }

#     return render(request, 'quarry/other/readonly.html', context=context)


# def submit_quarry(request, pk):
#     if request.method == 'POST':
#         quarry = get_object_or_404(Quarry, pk=pk)
#         quarry_approval = QuarryApproval.objects.create(
#             quarry=quarry, requestor=request.user)
#         return redirect('quarry:list')

#     else:
#         raise Http404


# def state_approve_quarry(request, pk):
#     if request.method == 'POST':
#         quarry = get_object_or_404(Quarry, pk=pk)
#         quarry_approval = quarry.get_last_approval()
#         quarry_approval.state_inspector = request.user
#         quarry_approval.state_approved = True
#         quarry_approval.save()
#         return redirect('quarry:list_state')

#     else:
#         raise Http404


# def state_reject_quarry(request, pk):
#     if request.method == 'POST':
#         quarry = get_object_or_404(Quarry, pk=pk)
#         quarry_approval = quarry.get_last_approval()
#         quarry_approval.state_inspector = request.user
#         quarry_approval.state_comment = request.POST.get('comment')
#         quarry_approval.state_approved = False
#         quarry_approval.save()
#         return redirect('quarry:list_state')

#     else:
#         raise Http404


# def state_admin_approve_quarry(request, pk):
#     if request.method == 'POST':
#         quarry = get_object_or_404(Quarry, pk=pk)
#         quarry_approval = quarry.get_last_approval()
#         quarry_approval.admin_inspector = request.user
#         quarry_approval.admin_approved = True
#         quarry_approval.save()
#         return redirect('quarry:list_state_admin')

#     else:
#         raise Http404


# def state_admin_reject_quarry(request, pk):
#     if request.method == 'POST':
#         quarry = get_object_or_404(Quarry, pk=pk)
#         quarry_approval = quarry.get_last_approval()
#         quarry_approval.admin_inspector = request.user
#         quarry_approval.admin_comment = request.POST.get('comment')
#         quarry_approval.admin_approved = False
#         quarry_approval.save()
#         return redirect('quarry:list_state_admin')

#     else:
#         raise Http404


# def get_comment_quarry(request, pk):
#     quarry = get_object_or_404(Quarry, pk=pk)
#     quarry_approval = quarry.get_last_approval()
#     if quarry_approval.admin_comment:
#         return HttpResponse(quarry_approval.admin_comment)
#     elif quarry_approval.state_comment:
#         return HttpResponse(quarry_approval.state_comment)
#     else:
#         return HttpResponse('')
