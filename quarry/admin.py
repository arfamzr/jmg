from django.contrib import admin

from .models import (
    LeaseHolder,
    Operator,
    QuarryManager,
    Quarry,
    Lot,
    MainRock,
    SideRock,
    Data,
    MainProductionStatistic,
    SideProductionStatistic,
    SalesSubmission,
    LocalFinalUses,
    ExportFinalUses,
    LocalOperator,
    ForeignOperator,
    LocalContractor,
    ForeignContractor,
    InternalCombustionMachinery,
    ElectricMachinery,
    DailyExplosive,
    EnergySupply,
    OperatingRecord,
    Royalties,
    Other,
    Approval,
)


@admin.register(LeaseHolder)
class LeaseHolderAdmin(admin.ModelAdmin):
    pass


@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    pass


@admin.register(QuarryManager)
class ManagerAdmin(admin.ModelAdmin):
    pass


@admin.register(Quarry)
class QuarryAdmin(admin.ModelAdmin):
    pass


@admin.register(Lot)
class LotAdmin(admin.ModelAdmin):
    pass


@admin.register(MainRock)
class MainRockAdmin(admin.ModelAdmin):
    pass


@admin.register(SideRock)
class SideRockAdmin(admin.ModelAdmin):
    pass


@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    pass


@admin.register(MainProductionStatistic)
class MainProductionStatisticAdmin(admin.ModelAdmin):
    pass


@admin.register(SideProductionStatistic)
class SideProductionStatisticAdmin(admin.ModelAdmin):
    pass


@admin.register(SalesSubmission)
class SalesSubmissionAdmin(admin.ModelAdmin):
    pass


@admin.register(LocalFinalUses)
class LocalFinalUsesAdmin(admin.ModelAdmin):
    pass


@admin.register(ExportFinalUses)
class ExportFinalUsesAdmin(admin.ModelAdmin):
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


@admin.register(DailyExplosive)
class DailyExplosiveAdmin(admin.ModelAdmin):
    pass


@admin.register(EnergySupply)
class EnergySupplyAdmin(admin.ModelAdmin):
    pass


@admin.register(OperatingRecord)
class OperatingRecordAdmin(admin.ModelAdmin):
    pass


@admin.register(Royalties)
class RoyaltiesAdmin(admin.ModelAdmin):
    pass


@admin.register(Other)
class OtherAdmin(admin.ModelAdmin):
    pass


@admin.register(Approval)
class ApprovalAdmin(admin.ModelAdmin):
    list_display = ['data', 'state_inspector',
                    'state_approved', 'admin_inspector', 'admin_approved']
    list_editable = ['state_inspector', 'state_approved',
                     'admin_inspector', 'admin_approved']


# admin.site.register(Quarry, QuarryAdmin)
# admin.site.register(QuarryMiner, QuarryMinerAdmin)
# admin.site.register(QuarryMinerData, QuarryMinerDataAdmin)
# admin.site.register(ProductionStatistic, ProductionStatisticAdmin)
# admin.site.register(SalesSubmission, SalesSubmissionAdmin)
# admin.site.register(LocalFinalUses, LocalFinalUsesAdmin)
# admin.site.register(ExportFinalUses, ExportFinalUsesAdmin)
# admin.site.register(LocalOperator, LocalOperatorAdmin)
# admin.site.register(ForeignOperator, ForeignOperatorAdmin)
# admin.site.register(LocalContractor, LocalContractorAdmin)
# admin.site.register(ForeignContractor, ForeignContractorAdmin)
# admin.site.register(InternalCombustionMachinery,
#                     InternalCombustionMachineryAdmin)
# admin.site.register(ElectricMachinery, ElectricMachineryAdmin)
# admin.site.register(DailyExplosive, DailyExplosiveAdmin)
# admin.site.register(EnergySupply, EnergySupplyAdmin)
# admin.site.register(OperatingRecord, OperatingRecordAdmin)
# admin.site.register(Royalties, RoyaltiesAdmin)
# admin.site.register(Other, OtherAdmin)
# admin.site.register(QuarryDataApproval, QuarryDataApprovalAdmin)
