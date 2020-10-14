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
