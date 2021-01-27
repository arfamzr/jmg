from django.contrib import admin

from .models import (
    ProcessFactory,
    ProcessManager,
    ProcessData,
    ProcessStatistic,
    ProcessSubmission,
    LocalOperator,
    ForeignOperator,
    LocalContractor,
    ForeignContractor,
    InternalCombustionMachinery,
    ElectricMachinery,
    EnergySupply,
    OperatingRecord,
    Other,
    Approval,
)


@admin.register(ProcessFactory)
class ProcessFactoryAdmin(admin.ModelAdmin):
    pass


@admin.register(ProcessManager)
class ProcessManagerAdmin(admin.ModelAdmin):
    pass


@admin.register(ProcessData)
class ProcessDataAdmin(admin.ModelAdmin):
    pass


@admin.register(ProcessStatistic)
class ProcessStatisticAdmin(admin.ModelAdmin):
    pass


@admin.register(ProcessSubmission)
class ProcessSubmissionAdmin(admin.ModelAdmin):
    pass


@admin.register(LocalOperator)
class LocalOperatorAdmin(admin.ModelAdmin):
    pass


@admin.register(ForeignOperator)
class ForeignOperatorAdmin(admin.ModelAdmin):
    pass


@admin.register(LocalContractor)
class LocalContractorAdmin(admin.ModelAdmin):
    pass


@admin.register(ForeignContractor)
class ForeignContractorAdmin(admin.ModelAdmin):
    pass


@admin.register(InternalCombustionMachinery)
class InternalCombustionMachineryAdmin(admin.ModelAdmin):
    pass


@admin.register(ElectricMachinery)
class ElectricMachineryAdmin(admin.ModelAdmin):
    pass


@admin.register(EnergySupply)
class EnergySupplyAdmin(admin.ModelAdmin):
    pass


@admin.register(OperatingRecord)
class OperatingRecordAdmin(admin.ModelAdmin):
    pass


@admin.register(Other)
class OtherAdmin(admin.ModelAdmin):
    pass


@admin.register(Approval)
class ApprovalAdmin(admin.ModelAdmin):
    pass
