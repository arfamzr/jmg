from django.contrib import admin

from .models import (
    LeaseHolder,
    Manager,
    Operator,
    Mine,
    MainMineral,
    SideMineral,
    Data,
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
    Approval,
)


@admin.register(LeaseHolder)
class LeaseHolderAdmin(admin.ModelAdmin):
    pass


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    pass


@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    pass


@admin.register(Mine)
class MineAdmin(admin.ModelAdmin):
    pass


@admin.register(MainMineral)
class MainMineralAdmin(admin.ModelAdmin):
    pass


@admin.register(SideMineral)
class SideMineralAdmin(admin.ModelAdmin):
    pass


@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    pass


@admin.register(MainStatistic)
class MainStatisticAdmin(admin.ModelAdmin):
    pass


@admin.register(SideStatistic)
class SideStatisticAdmin(admin.ModelAdmin):
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


@admin.register(Approval)
class ApprovalAdmin(admin.ModelAdmin):
    list_display = ['data', 'state_inspector',
                    'state_approved', 'admin_inspector', 'admin_approved']
    list_editable = ['state_inspector', 'state_approved',
                     'admin_inspector', 'admin_approved']


# admin.site.register(Mine, MineAdmin)
# admin.site.register(LeaseHolder, LeaseHolderAdmin)
# admin.site.register(Operator, OperatorAdmin)
# admin.site.register(MineMiner, MineMinerAdmin)
# admin.site.register(MineMinerData, MineMinerDataAdmin)
# admin.site.register(MainStatistic, MainStatisticAdmin)
# admin.site.register(SideStatistic, SideStatisticAdmin)
# admin.site.register(LocalOperator, LocalOperatorAdmin)
# admin.site.register(ForeignOperator, ForeignOperatorAdmin)
# admin.site.register(LocalContractor, LocalContractorAdmin)
# admin.site.register(ForeignContractor, ForeignContractorAdmin)
# admin.site.register(InternalCombustionMachinery,
#                     InternalCombustionMachineryAdmin)
# admin.site.register(ElectricMachinery, ElectricMachineryAdmin)
# admin.site.register(EnergySupply, EnergySupplyAdmin)
# admin.site.register(OperatingRecord, OperatingRecordAdmin)
# admin.site.register(MineDataApproval, MineDataApprovalAdmin)
