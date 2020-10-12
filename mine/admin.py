from django.contrib import admin

from .models import (
    Mine,
    Statistic,
    LocalOperator,
    ForeignOperator,
    LocalContractor,
    ForeignContractor,
    InternalCombustionMachinery,
    ElectricMachinery,
    EnergySupply,
    OperatingRecord,
    MineApproval,
)


class MineAdmin(admin.ModelAdmin):
    pass


class StatisticAdmin(admin.ModelAdmin):
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


class EnergySupplyAdmin(admin.ModelAdmin):
    pass


class OperatingRecordAdmin(admin.ModelAdmin):
    pass


class MineApprovalAdmin(admin.ModelAdmin):
    pass


admin.site.register(Mine, MineAdmin)
admin.site.register(Statistic, StatisticAdmin)
admin.site.register(LocalOperator, LocalOperatorAdmin)
admin.site.register(ForeignOperator, ForeignOperatorAdmin)
admin.site.register(LocalContractor, LocalContractorAdmin)
admin.site.register(ForeignContractor, ForeignContractorAdmin)
admin.site.register(InternalCombustionMachinery,
                    InternalCombustionMachineryAdmin)
admin.site.register(ElectricMachinery, ElectricMachineryAdmin)
admin.site.register(EnergySupply, EnergySupplyAdmin)
admin.site.register(OperatingRecord, OperatingRecordAdmin)
admin.site.register(MineApproval, MineApprovalAdmin)
