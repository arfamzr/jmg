from django.contrib import admin

from .models import (
    Mine,
    MineMiner,
    MineMinerData,
    MainStatistic,
    SideStatistic,
    LocalOperator,
    ForeignOperator,
    LocalContractor,
    ForeignContractor,
    InternalCombustionMachinery,
    ElectricMachinery,
    EnergySupply,
    OperatingRecord,
    MineDataApproval,
)


class MineAdmin(admin.ModelAdmin):
    pass


class MineMinerAdmin(admin.ModelAdmin):
    pass


class MineMinerDataAdmin(admin.ModelAdmin):
    pass


class MainStatisticAdmin(admin.ModelAdmin):
    pass


class SideStatisticAdmin(admin.ModelAdmin):
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


class MineDataApprovalAdmin(admin.ModelAdmin):
    list_display = ['miner_data', 'state_inspector',
                    'state_approved', 'admin_inspector', 'admin_approved']
    list_editable = ['state_inspector', 'state_approved',
                     'admin_inspector', 'admin_approved']


admin.site.register(Mine, MineAdmin)
admin.site.register(MineMiner, MineMinerAdmin)
admin.site.register(MineMinerData, MineMinerDataAdmin)
admin.site.register(MainStatistic, MainStatisticAdmin)
admin.site.register(SideStatistic, SideStatisticAdmin)
admin.site.register(LocalOperator, LocalOperatorAdmin)
admin.site.register(ForeignOperator, ForeignOperatorAdmin)
admin.site.register(LocalContractor, LocalContractorAdmin)
admin.site.register(ForeignContractor, ForeignContractorAdmin)
admin.site.register(InternalCombustionMachinery,
                    InternalCombustionMachineryAdmin)
admin.site.register(ElectricMachinery, ElectricMachineryAdmin)
admin.site.register(EnergySupply, EnergySupplyAdmin)
admin.site.register(OperatingRecord, OperatingRecordAdmin)
admin.site.register(MineDataApproval, MineDataApprovalAdmin)
