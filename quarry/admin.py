from django.contrib import admin

from .models import (
    Quarry,
    ProductionStatistic,
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
    QuarryApproval,
)


class QuarryAdmin(admin.ModelAdmin):
    pass


class ProductionStatisticAdmin(admin.ModelAdmin):
    pass


class SalesSubmissionAdmin(admin.ModelAdmin):
    pass


class LocalFinalUsesAdmin(admin.ModelAdmin):
    pass


class ExportFinalUsesAdmin(admin.ModelAdmin):
    pass


class LocalOperatorAdmin(admin.ModelAdmin):
    pass


class ForeignOperatorAdmin(admin.ModelAdmin):
    pass


class LocalContractorAdmin(admin.ModelAdmin):
    pass


class ForeignContractorAdmin(admin.ModelAdmin):
    pass


class InternalCombustionMachineryAdmin(admin.ModelAdmin):
    pass


class ElectricMachineryAdmin(admin.ModelAdmin):
    pass


class DailyExplosiveAdmin(admin.ModelAdmin):
    pass


class EnergySupplyAdmin(admin.ModelAdmin):
    pass


class OperatingRecordAdmin(admin.ModelAdmin):
    pass


class RoyaltiesAdmin(admin.ModelAdmin):
    pass


class OtherAdmin(admin.ModelAdmin):
    pass


class QuarryApprovalAdmin(admin.ModelAdmin):
    pass


admin.site.register(Quarry, QuarryAdmin)
admin.site.register(ProductionStatistic, ProductionStatisticAdmin)
admin.site.register(SalesSubmission, SalesSubmissionAdmin)
admin.site.register(LocalFinalUses, LocalFinalUsesAdmin)
admin.site.register(ExportFinalUses, ExportFinalUsesAdmin)
admin.site.register(LocalOperator, LocalOperatorAdmin)
admin.site.register(ForeignOperator, ForeignOperatorAdmin)
admin.site.register(LocalContractor, LocalContractorAdmin)
admin.site.register(ForeignContractor, ForeignContractorAdmin)
admin.site.register(InternalCombustionMachinery,
                    InternalCombustionMachineryAdmin)
admin.site.register(ElectricMachinery, ElectricMachineryAdmin)
admin.site.register(DailyExplosive, DailyExplosiveAdmin)
admin.site.register(EnergySupply, EnergySupplyAdmin)
admin.site.register(OperatingRecord, OperatingRecordAdmin)
admin.site.register(Royalties, RoyaltiesAdmin)
admin.site.register(Other, OtherAdmin)
admin.site.register(QuarryApproval, QuarryApprovalAdmin)
