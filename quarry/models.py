from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

import datetime

from account.models import User, Profile


YEAR_CHOICES = [(year, year) for year in range(
    datetime.date.today().year-5, datetime.date.today().year+1)]


def current_year():
    return datetime.date.today().year


class Quarry(models.Model):
    address1 = models.CharField(_("alamat"), max_length=255)
    address2 = models.CharField(
        _("alamat (line 2)"), max_length=255, blank=True)
    address3 = models.CharField(
        _("alamat (line 3)"), max_length=255, blank=True)
    phone_number = models.CharField(_("no tel"), max_length=15)
    fax_number = models.CharField(_("no fax"), max_length=15)
    email = models.EmailField(_("email"), max_length=254)
    location = models.CharField(_("lokasi"), max_length=255)
    mukim = models.CharField(_("mukim"), max_length=255)
    district = models.CharField(_("daerah"), max_length=255)
    state = models.CharField(_("negeri"), max_length=3,
                             choices=Profile.STATE_CHOICES)
    land_status = models.CharField(_("status tanah"), max_length=255)
    grid_reference = models.CharField(_("rujukan grid"), max_length=255)
    max_capacity = models.CharField(_("keupayaan maksima"), max_length=255)
    company_category = models.CharField(_("kategori syarikat"), max_length=255)
    main_rock_type = models.CharField(_("jenis batuan utama"), max_length=255)
    side_rock_type = models.CharField(
        _("jenis batuan sampingan"), max_length=255)
    status = models.BooleanField(_("status"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "kuari"
        verbose_name_plural = "kuari"

    def __str__(self):
        return f'{self.location}, {self.mukim}, {self.district}, {self.get_state_display()}'

    def get_absolute_url(self):
        return reverse("quarry:state_admin:detail", kwargs={"pk": self.pk})

    def get_state_absolute_url(self):
        return reverse("quarry:state:detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("quarry:state_admin:update", kwargs={"pk": self.pk})

    def get_toggle_active_url(self):
        return reverse("quarry:state_admin:toggle_active", kwargs={"pk": self.pk})

    def get_add_miner_url(self):
        return reverse("quarry:state_admin:add_miner", kwargs={"pk": self.pk})


class QuarryMiner(models.Model):
    miner = models.ForeignKey(User, verbose_name=_(
        "pengusaha"), on_delete=models.CASCADE, related_name='quarries_mined')
    quarry = models.ForeignKey(Quarry, verbose_name=_(
        "kuari"), on_delete=models.CASCADE, related_name="miners")
    add_by = models.ForeignKey(User, verbose_name=_(
        "add by"), on_delete=models.SET_NULL, related_name='quarry_miners_added', null=True)
    lot_number = models.CharField(_("no lot"), max_length=255)
    latitude = models.DecimalField(
        _("latitude"), max_digits=15, decimal_places=4)
    longitude = models.DecimalField(
        _("longitude"), max_digits=15, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "pengusaha kuari"
        verbose_name_plural = "pengusaha kuari"

    def __str__(self):
        return f'{self.miner} ({self.quarry})'

    def get_delete_url(self):
        return reverse("quarry:state_admin:quarry_remove_miner", kwargs={"pk": self.pk})

    def get_add_report_url(self):
        return reverse("quarry:add_report", kwargs={"pk": self.pk})


class QuarryMinerData(models.Model):
    JAN = 1
    FEB = 2
    MAR = 3
    APR = 4
    MAY = 5
    JUN = 6
    JUL = 7
    AUG = 8
    SEP = 9
    OCT = 10
    NOV = 11
    DEC = 12
    MONTH_CHOICES = [
        (JAN, _('Januari')),
        (FEB, _('Februari')),
        (MAR, _('Mac')),
        (APR, _('April')),
        (MAY, _('Mei')),
        (JUN, _('Jun')),
        (JUL, _('Julai')),
        (AUG, _('Ogos')),
        (SEP, _('September')),
        (OCT, _('Oktober')),
        (NOV, _('November')),
        (DEC, _('Disember')),
    ]
    miner = models.ForeignKey(QuarryMiner, verbose_name=_(
        "pengusaha"), on_delete=models.SET_NULL, related_name='data', null=True)
    quarry = models.ForeignKey(Quarry, verbose_name=_(
        "kuari"), on_delete=models.SET_NULL, related_name='miner_data', null=True)
    state = models.CharField(_("negeri"), max_length=3,
                             choices=Profile.STATE_CHOICES)
    month = models.PositiveIntegerField(_("bulan"), choices=MONTH_CHOICES)
    year = models.PositiveIntegerField(
        _("tahun"), choices=YEAR_CHOICES, default=current_year)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "data pengusaha kuari"
        verbose_name_plural = "data pengusaha kuari"

    def __str__(self):
        return f'{self.miner} - {self.pk}'

    def get_absolute_url(self):
        return reverse("quarry:miner_data", kwargs={"pk": self.pk})

    def get_state_absolute_url(self):
        return reverse("quarry:state:miner_data", kwargs={"pk": self.pk})

    def get_state_admin_absolute_url(self):
        return reverse("quarry:state_admin:miner_data", kwargs={"pk": self.pk})

    def get_edit_url(self):
        return reverse("quarry:production_statistic_edit", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("quarry:miner_data_delete", kwargs={"pk": self.pk})

    def get_last_approval(self):
        return self.approvals.last()


class ProductionStatistic(models.Model):
    miner_data = models.OneToOneField(QuarryMinerData, verbose_name=_(
        "miner data"), on_delete=models.CASCADE, primary_key=True)
    initial_main_rock_stock = models.DecimalField(
        _("stok awal bulan batuan utama"), max_digits=15, decimal_places=4)
    initial_side_rock_stock = models.DecimalField(
        _("stok awal bulan batuan sampingan"), max_digits=15, decimal_places=4)
    main_rock_production = models.DecimalField(
        _("pengeluaran batuan utama"), max_digits=15, decimal_places=4)
    side_rock_production = models.DecimalField(
        _("pengeluaran batuan sampingan"), max_digits=15, decimal_places=4)
    total_main_rock = models.DecimalField(
        _("jumlah batuan utama"), max_digits=15, decimal_places=4)
    total_side_rock = models.DecimalField(
        _("jumlah batuan sampingan"), max_digits=15, decimal_places=4)
    main_rock_submission = models.DecimalField(
        _("penyerahan batuan utama"), max_digits=15, decimal_places=4)
    side_rock_submission = models.DecimalField(
        _("penyerahan batuan sampingan"), max_digits=15, decimal_places=4)
    final_main_rock_stock = models.DecimalField(
        _("stok akhir batuan utama"), max_digits=15, decimal_places=4)
    final_side_rock_stock = models.DecimalField(
        _("stok akhir batuan sampingan"), max_digits=15, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "perangkaan pengeluaran"
        verbose_name_plural = "perangkaan pengeluaran"

    def __str__(self):
        return f"{self.miner_data}"


class SalesSubmission(models.Model):
    miner_data = models.OneToOneField(QuarryMinerData, verbose_name=_(
        "miner data"), on_delete=models.CASCADE, primary_key=True)
    crusher_amount = models.DecimalField(
        _("amaun crusher run"), max_digits=15, decimal_places=4)
    crusher_worth = models.DecimalField(
        _("nilai crusher run"), max_digits=15, decimal_places=2)
    dust_amount = models.DecimalField(
        _("amaun quarry dust"), max_digits=15, decimal_places=4)
    dust_worth = models.DecimalField(
        _("nilai quarry dust"), max_digits=15, decimal_places=2)
    waste_amount = models.DecimalField(
        _("amaun quarry waste"), max_digits=15, decimal_places=4)
    waste_worth = models.DecimalField(
        _("nilai quarry waste"), max_digits=15, decimal_places=2)
    inch_1_8_amount = models.DecimalField(
        _("amaun 1/8\""), max_digits=15, decimal_places=4)
    inch_1_8_worth = models.DecimalField(
        _("nilai 1/8\""), max_digits=15, decimal_places=2)
    inch_3_8_amount = models.DecimalField(
        _("amaun 3/8\""), max_digits=15, decimal_places=4)
    inch_3_8_worth = models.DecimalField(
        _("nilai 3/8\""), max_digits=15, decimal_places=2)
    inch_5_8_amount = models.DecimalField(
        _("amaun 5/8\""), max_digits=15, decimal_places=4)
    inch_5_8_worth = models.DecimalField(
        _("nilai 5/8\""), max_digits=15, decimal_places=2)
    inch_3_4_amount = models.DecimalField(
        _("amaun 3/4\""), max_digits=15, decimal_places=4)
    inch_3_4_worth = models.DecimalField(
        _("nilai 3/4\""), max_digits=15, decimal_places=2)
    inch_1_amount = models.DecimalField(
        _("amaun 1\""), max_digits=15, decimal_places=4)
    inch_1_worth = models.DecimalField(
        _("nilai 1\""), max_digits=15, decimal_places=2)
    inch_1_1_2_amount = models.DecimalField(
        _("amaun 1 1/2\""), max_digits=15, decimal_places=4)
    inch_1_1_2_worth = models.DecimalField(
        _("nilai 1 1/2\""), max_digits=15, decimal_places=2)
    inch_2_amount = models.DecimalField(
        _("amaun 2\""), max_digits=15, decimal_places=4)
    inch_2_worth = models.DecimalField(
        _("nilai 2\""), max_digits=15, decimal_places=2)
    inch_3x5_amount = models.DecimalField(
        _("amaun 3\" x 5\""), max_digits=15, decimal_places=4)
    inch_3x5_worth = models.DecimalField(
        _("nilai 3\" x 5\""), max_digits=15, decimal_places=2)
    inch_6x9_amount = models.DecimalField(
        _("amaun 6\" x 9\""), max_digits=15, decimal_places=4)
    inch_6x9_worth = models.DecimalField(
        _("nilai 6\" x 9\""), max_digits=15, decimal_places=2)
    block_amount = models.DecimalField(
        _("amaun block"), max_digits=15, decimal_places=4)
    block_worth = models.DecimalField(
        _("nilai block"), max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "penyerahan jualan"
        verbose_name_plural = "penyerahan jualan"

    def __str__(self):
        return f"{self.miner_data}"


class LocalFinalUses(models.Model):
    miner_data = models.OneToOneField(QuarryMinerData, verbose_name=_(
        "miner data"), on_delete=models.CASCADE, primary_key=True)
    construction_amount = models.DecimalField(
        _("amaun pembinaan"), max_digits=15, decimal_places=4)
    construction_worth = models.DecimalField(
        _("nilai pembinaan"), max_digits=15, decimal_places=2)
    dimension_stone_amount = models.DecimalField(
        _("amaun batu dimensi"), max_digits=15, decimal_places=4)
    dimension_stone_worth = models.DecimalField(
        _("nilai batu dimensi"), max_digits=15, decimal_places=2)
    cement_making_amount = models.DecimalField(
        _("amaun pembuatan simen"), max_digits=15, decimal_places=4)
    cement_making_worth = models.DecimalField(
        _("nilai pembuatan simen"), max_digits=15, decimal_places=2)
    quicklime_amount = models.DecimalField(
        _("amaun kapur tohor"), max_digits=15, decimal_places=4)
    quicklime_worth = models.DecimalField(
        _("nilai kapur tohor"), max_digits=15, decimal_places=2)
    calcium_carbonate_powder_amount = models.DecimalField(
        _("amaun serbuk kalsium karbonat"), max_digits=15, decimal_places=4)
    calcium_carbonate_powder_worth = models.DecimalField(
        _("nilai serbuk kalsium karbonat"), max_digits=15, decimal_places=2)
    premix_amount = models.DecimalField(
        _("amaun premix"), max_digits=15, decimal_places=4)
    premix_worth = models.DecimalField(
        _("nilai premix"), max_digits=15, decimal_places=2)
    ready_mix_concrete_amount = models.DecimalField(
        _("amaun konkrit readymix"), max_digits=15, decimal_places=4)
    ready_mix_concrete_worth = models.DecimalField(
        _("nilai konkrit readymix"), max_digits=15, decimal_places=2)
    fertilizer_amount = models.DecimalField(
        _("amaun baja"), max_digits=15, decimal_places=4)
    fertilizer_worth = models.DecimalField(
        _("nilai baja"), max_digits=15, decimal_places=2)
    steel_amount = models.DecimalField(
        _("amaun industri keluli"), max_digits=15, decimal_places=4)
    steel_worth = models.DecimalField(
        _("nilai industri keluli"), max_digits=15, decimal_places=2)
    hydrated_lime_amount = models.DecimalField(
        _("amaun kapur hidrat"), max_digits=15, decimal_places=4)
    hydrated_lime_worth = models.DecimalField(
        _("nilai kapur hidrat"), max_digits=15, decimal_places=2)
    dolomite_powder_amount = models.DecimalField(
        _("amaun serbuk dolomit"), max_digits=15, decimal_places=4)
    dolomite_powder_worth = models.DecimalField(
        _("nilai serbuk dolomit"), max_digits=15, decimal_places=2)
    terrazo_amount = models.DecimalField(
        _("amaun terazo"), max_digits=15, decimal_places=4)
    terrazo_worth = models.DecimalField(
        _("nilai terazo"), max_digits=15, decimal_places=2)
    other_amount = models.DecimalField(
        _("amaun lain"), max_digits=15, decimal_places=4)
    other_worth = models.DecimalField(
        _("nilai lain"), max_digits=15, decimal_places=2)
    state_other = models.TextField(_("nyatakan lain"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "kegunaan akhir tempatan"
        verbose_name_plural = "kegunaan akhir tempatan"

    def __str__(self):
        return f"{self.miner_data}"


class ExportFinalUses(models.Model):
    miner_data = models.OneToOneField(QuarryMinerData, verbose_name=_(
        "miner data"), on_delete=models.CASCADE, primary_key=True)
    construction_amount = models.DecimalField(
        _("amaun pembinaan"), max_digits=15, decimal_places=4)
    construction_worth = models.DecimalField(
        _("nilai pembinaan"), max_digits=15, decimal_places=2)
    dimension_stone_amount = models.DecimalField(
        _("amaun batu dimensi"), max_digits=15, decimal_places=4)
    dimension_stone_worth = models.DecimalField(
        _("nilai batu dimensi"), max_digits=15, decimal_places=2)
    cement_making_amount = models.DecimalField(
        _("amaun pembuatan simen"), max_digits=15, decimal_places=4)
    cement_making_worth = models.DecimalField(
        _("nilai pembuatan simen"), max_digits=15, decimal_places=2)
    quicklime_amount = models.DecimalField(
        _("amaun kapur tohor"), max_digits=15, decimal_places=4)
    quicklime_worth = models.DecimalField(
        _("nilai kapur tohor"), max_digits=15, decimal_places=2)
    calcium_carbonate_powder_amount = models.DecimalField(
        _("amaun serbuk kalsium karbonat"), max_digits=15, decimal_places=4)
    calcium_carbonate_powder_worth = models.DecimalField(
        _("nilai serbuk kalsium karbonat"), max_digits=15, decimal_places=2)
    premix_amount = models.DecimalField(
        _("amaun premix"), max_digits=15, decimal_places=4)
    premix_worth = models.DecimalField(
        _("nilai premix"), max_digits=15, decimal_places=2)
    ready_mix_concrete_amount = models.DecimalField(
        _("amaun konkrit readymix"), max_digits=15, decimal_places=4)
    ready_mix_concrete_worth = models.DecimalField(
        _("nilai konkrit readymix"), max_digits=15, decimal_places=2)
    fertilizer_amount = models.DecimalField(
        _("amaun baja"), max_digits=15, decimal_places=4)
    fertilizer_worth = models.DecimalField(
        _("nilai baja"), max_digits=15, decimal_places=2)
    steel_amount = models.DecimalField(
        _("amaun industri keluli"), max_digits=15, decimal_places=4)
    steel_worth = models.DecimalField(
        _("nilai industri keluli"), max_digits=15, decimal_places=2)
    hydrated_lime_amount = models.DecimalField(
        _("amaun kapur hidrat"), max_digits=15, decimal_places=4)
    hydrated_lime_worth = models.DecimalField(
        _("nilai kapur hidrat"), max_digits=15, decimal_places=2)
    dolomite_powder_amount = models.DecimalField(
        _("amaun serbuk dolomit"), max_digits=15, decimal_places=4)
    dolomite_powder_worth = models.DecimalField(
        _("nilai serbuk dolomit"), max_digits=15, decimal_places=2)
    terrazo_amount = models.DecimalField(
        _("amaun terazo"), max_digits=15, decimal_places=4)
    terrazo_worth = models.DecimalField(
        _("nilai terazo"), max_digits=15, decimal_places=2)
    other_amount = models.DecimalField(
        _("amaun lain"), max_digits=15, decimal_places=4)
    other_worth = models.DecimalField(
        _("nilai lain"), max_digits=15, decimal_places=2)
    state_other = models.TextField(_("nyatakan lain"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "kegunaan akhir eksport"
        verbose_name_plural = "kegunaan akhir eksport"

    def __str__(self):
        return f"{self.miner_data}"


class LocalOperator(models.Model):
    miner_data = models.OneToOneField(QuarryMinerData, verbose_name=_(
        "miner data"), on_delete=models.CASCADE, primary_key=True)
    male_manager = models.IntegerField(_("pengurus lelaki"))
    female_manager = models.IntegerField(_("pengurus perempuan"))
    male_professional = models.IntegerField(_("profesional lelaki"))
    female_professional = models.IntegerField(_("profesional perempuan"))
    male_technical = models.IntegerField(_("teknikal lelaki"))
    female_technical = models.IntegerField(_("teknikal perempuan"))
    male_clerk = models.IntegerField(_("kerani lelaki"))
    female_clerk = models.IntegerField(_("kerani perempuan"))
    male_labor = models.IntegerField(_("buruh lelaki"))
    female_labor = models.IntegerField(_("buruh perempuan"))
    total_female = models.IntegerField(_("jumlah perempuan"))
    total_male = models.IntegerField(_("jumlah lelaki"))
    total_male_salary = models.DecimalField(
        _("jumlah upah gaji lelaki"), max_digits=15, decimal_places=2)
    total_female_salary = models.DecimalField(
        _("jumlah upah gaji perempuan"), max_digits=15, decimal_places=2)
    male_man_hour = models.IntegerField(_("jam manusia lelaki"))
    female_man_hour = models.IntegerField(_("jam manusia perempuan"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "operator tempatan"
        verbose_name_plural = "operator tempatan"

    def __str__(self):
        return f"{self.miner_data}"


class ForeignOperator(models.Model):
    miner_data = models.OneToOneField(QuarryMinerData, verbose_name=_(
        "miner data"), on_delete=models.CASCADE, primary_key=True)
    male_manager = models.IntegerField(_("pengurus lelaki"))
    female_manager = models.IntegerField(_("pengurus perempuan"))
    male_professional = models.IntegerField(_("profesional lelaki"))
    female_professional = models.IntegerField(_("profesional perempuan"))
    male_technical = models.IntegerField(_("teknikal lelaki"))
    female_technical = models.IntegerField(_("teknikal perempuan"))
    male_clerk = models.IntegerField(_("kerani lelaki"))
    female_clerk = models.IntegerField(_("kerani perempuan"))
    male_labor = models.IntegerField(_("buruh lelaki"))
    female_labor = models.IntegerField(_("buruh perempuan"))
    total_female = models.IntegerField(_("jumlah perempuan"))
    total_male = models.IntegerField(_("jumlah lelaki"))
    total_male_salary = models.DecimalField(
        _("jumlah upah gaji lelaki"), max_digits=15, decimal_places=2)
    total_female_salary = models.DecimalField(
        _("jumlah upah gaji perempuan"), max_digits=15, decimal_places=2)
    male_man_hour = models.IntegerField(_("jam manusia lelaki"))
    female_man_hour = models.IntegerField(_("jam manusia perempuan"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "operator asing"
        verbose_name_plural = "operator asing"

    def __str__(self):
        return f"{self.miner_data}"


class LocalContractor(models.Model):
    miner_data = models.OneToOneField(QuarryMinerData, verbose_name=_(
        "miner data"), on_delete=models.CASCADE, primary_key=True)
    male_manager = models.IntegerField(_("pengurus lelaki"))
    female_manager = models.IntegerField(_("pengurus perempuan"))
    male_professional = models.IntegerField(_("profesional lelaki"))
    female_professional = models.IntegerField(_("profesional perempuan"))
    male_technical = models.IntegerField(_("teknikal lelaki"))
    female_technical = models.IntegerField(_("teknikal perempuan"))
    male_clerk = models.IntegerField(_("kerani lelaki"))
    female_clerk = models.IntegerField(_("kerani perempuan"))
    male_labor = models.IntegerField(_("buruh lelaki"))
    female_labor = models.IntegerField(_("buruh perempuan"))
    total_female = models.IntegerField(_("jumlah perempuan"))
    total_male = models.IntegerField(_("jumlah lelaki"))
    total_male_salary = models.DecimalField(
        _("jumlah upah gaji lelaki"), max_digits=15, decimal_places=2)
    total_female_salary = models.DecimalField(
        _("jumlah upah gaji perempuan"), max_digits=15, decimal_places=2)
    male_man_hour = models.IntegerField(_("jam manusia lelaki"))
    female_man_hour = models.IntegerField(_("jam manusia perempuan"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "kontraktor tempatan"
        verbose_name_plural = "kontraktor tempatan"

    def __str__(self):
        return f"{self.miner_data}"


class ForeignContractor(models.Model):
    miner_data = models.OneToOneField(QuarryMinerData, verbose_name=_(
        "miner data"), on_delete=models.CASCADE, primary_key=True)
    male_manager = models.IntegerField(_("pengurus lelaki"))
    female_manager = models.IntegerField(_("pengurus perempuan"))
    male_professional = models.IntegerField(_("profesional lelaki"))
    female_professional = models.IntegerField(_("profesional perempuan"))
    male_technical = models.IntegerField(_("teknikal lelaki"))
    female_technical = models.IntegerField(_("teknikal perempuan"))
    male_clerk = models.IntegerField(_("kerani lelaki"))
    female_clerk = models.IntegerField(_("kerani perempuan"))
    male_labor = models.IntegerField(_("buruh lelaki"))
    female_labor = models.IntegerField(_("buruh perempuan"))
    total_female = models.IntegerField(_("jumlah perempuan"))
    total_male = models.IntegerField(_("jumlah lelaki"))
    total_male_salary = models.DecimalField(
        _("jumlah upah gaji lelaki"), max_digits=15, decimal_places=2)
    total_female_salary = models.DecimalField(
        _("jumlah upah gaji perempuan"), max_digits=15, decimal_places=2)
    male_man_hour = models.IntegerField(_("jam manusia lelaki"))
    female_man_hour = models.IntegerField(_("jam manusia perempuan"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "kontraktor asing"
        verbose_name_plural = "kontraktor asing"

    def __str__(self):
        return f"{self.miner_data}"


class InternalCombustionMachinery(models.Model):
    miner_data = models.OneToOneField(QuarryMinerData, verbose_name=_(
        "miner data"), on_delete=models.CASCADE, primary_key=True)
    number_lorry = models.IntegerField(_("bilangan lori"))
    lorry_power = models.DecimalField(
        _("kuasa lori"), max_digits=15, decimal_places=2)
    number_excavator = models.IntegerField(_("bilangan jenkorek"))
    excavator_power = models.DecimalField(
        _("kuasa jenkorek"), max_digits=15, decimal_places=2)
    number_wheel_loader = models.IntegerField(
        _("bilangan jentera angkut beroda"))
    wheel_loader_power = models.DecimalField(
        _("kuasa jentera angkut beroda"), max_digits=15, decimal_places=2)
    number_bulldozer = models.IntegerField(_("bilangan jentolak"))
    bulldozer_power = models.DecimalField(
        _("kuasa jentolak"), max_digits=15, decimal_places=2)
    number_water_pump = models.IntegerField(_("bilangan pam air"))
    water_pump_power = models.DecimalField(
        _("kuasa pam air"), max_digits=15, decimal_places=2)
    number_air_compressor = models.IntegerField(_("bilangan pemampat udara"))
    air_compressor_power = models.DecimalField(
        _("kuasa pemampat udara"), max_digits=15, decimal_places=2)
    number_hydraulic_breaker = models.IntegerField(
        _("bilangan pemecah hidraulik"))
    hydraulic_breaker_power = models.DecimalField(
        _("kuasa pemecah hidraulik"), max_digits=15, decimal_places=2)
    number_hydraulic_drill = models.IntegerField(
        _("bilangan gerudi hidraulik"))
    hydraulic_drill_power = models.DecimalField(
        _("kuasa gerudi hidraulik"), max_digits=15, decimal_places=2)
    number_crusher = models.IntegerField(_("bilangan penghancur"))
    crusher_power = models.DecimalField(
        _("kuasa penghancur"), max_digits=15, decimal_places=2)
    number_shovel = models.IntegerField(_("bilangan penyuduk"))
    shovel_power = models.DecimalField(
        _("kuasa penyuduk"), max_digits=15, decimal_places=2)
    number_tracktor = models.IntegerField(_("bilangan traktor"))
    tracktor_power = models.DecimalField(
        _("kuasa traktor"), max_digits=15, decimal_places=2)
    number_other = models.IntegerField(_("bilangan lain"))
    other_power = models.DecimalField(
        _("kuasa lain"), max_digits=15, decimal_places=2)
    state_other = models.TextField(_("nyatakan lain"), blank=True)
    total_number = models.IntegerField(_("jumlah bilangan"))
    total_power = models.DecimalField(
        _("jumlah_kuasa"), max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "jentera bakar dalam"
        verbose_name_plural = "jentera bakar dalam"

    def __str__(self):
        return f"{self.miner_data}"


class ElectricMachinery(models.Model):
    miner_data = models.OneToOneField(QuarryMinerData, verbose_name=_(
        "miner data"), on_delete=models.CASCADE, primary_key=True)
    number_lorry = models.IntegerField(_("bilangan lori"))
    lorry_power = models.DecimalField(
        _("kuasa lori"), max_digits=15, decimal_places=2)
    number_excavator = models.IntegerField(_("bilangan jenkorek"))
    excavator_power = models.DecimalField(
        _("kuasa jenkorek"), max_digits=15, decimal_places=2)
    number_wheel_loader = models.IntegerField(
        _("bilangan jentera angkut beroda"))
    wheel_loader_power = models.DecimalField(
        _("kuasa jentera angkut beroda"), max_digits=15, decimal_places=2)
    number_bulldozer = models.IntegerField(_("bilangan jentolak"))
    bulldozer_power = models.DecimalField(
        _("kuasa jentolak"), max_digits=15, decimal_places=2)
    number_water_pump = models.IntegerField(_("bilangan pam air"))
    water_pump_power = models.DecimalField(
        _("kuasa pam air"), max_digits=15, decimal_places=2)
    number_air_compressor = models.IntegerField(_("bilangan pemampat udara"))
    air_compressor_power = models.DecimalField(
        _("kuasa pemampat udara"), max_digits=15, decimal_places=2)
    number_hydraulic_breaker = models.IntegerField(
        _("bilangan pemecah hidraulik"))
    hydraulic_breaker_power = models.DecimalField(
        _("kuasa pemecah hidraulik"), max_digits=15, decimal_places=2)
    number_hydraulic_drill = models.IntegerField(
        _("bilangan gerudi hidraulik"))
    hydraulic_drill_power = models.DecimalField(
        _("kuasa gerudi hidraulik"), max_digits=15, decimal_places=2)
    number_crusher = models.IntegerField(_("bilangan penghancur"))
    crusher_power = models.DecimalField(
        _("kuasa penghancur"), max_digits=15, decimal_places=2)
    number_shovel = models.IntegerField(_("bilangan penyuduk"))
    shovel_power = models.DecimalField(
        _("kuasa penyuduk"), max_digits=15, decimal_places=2)
    number_tracktor = models.IntegerField(_("bilangan traktor"))
    tracktor_power = models.DecimalField(
        _("kuasa traktor"), max_digits=15, decimal_places=2)
    number_other = models.IntegerField(_("bilangan lain"))
    other_power = models.DecimalField(
        _("kuasa lain"), max_digits=15, decimal_places=2)
    state_other = models.TextField(_("nyatakan lain"), blank=True)
    total_number = models.IntegerField(_("jumlah bilangan"))
    total_power = models.DecimalField(
        _("jumlah_kuasa"), max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "jentera elektrik"
        verbose_name_plural = "jentera elektrik"

    def __str__(self):
        return f"{self.miner_data}"


class DailyExplosive(models.Model):
    miner_data = models.ForeignKey(QuarryMinerData, verbose_name=_(
        "miner data"), on_delete=models.CASCADE, related_name='daily_explosives')
    date = models.DateField(_("tarikh"))
    emulsion_explosive = models.DecimalField(
        _("bahan letupan bes emulsi"), max_digits=15, decimal_places=2)
    ng_explosive = models.DecimalField(
        _("bahan letupan bes ng"), max_digits=15, decimal_places=2)
    other_explosive = models.DecimalField(
        _("bahan letupan lain"), max_digits=15, decimal_places=2)
    detonator = models.IntegerField(_("peledak biasa"))
    electric_detonator = models.IntegerField(_("peledak elektrik"))
    non_electric_detonator = models.IntegerField(_("peledak non elektrik"))
    safety_fuse = models.DecimalField(
        _("safety fuse"), max_digits=15, decimal_places=2)
    detonating_cord = models.DecimalField(
        _("kord peledak"), max_digits=15, decimal_places=2)
    anfo = models.DecimalField(_("ANFO"), max_digits=15, decimal_places=2)
    bulk_emulsion = models.DecimalField(
        _("bulk emulsion"), max_digits=15, decimal_places=2)
    relay_tld = models.IntegerField(_("relay TLD"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "bahan letupan harian"
        verbose_name_plural = "bahan letupan harian"

    def __str__(self):
        return f'{self.miner_data} ({self.pk})'


class EnergySupply(models.Model):
    miner_data = models.OneToOneField(QuarryMinerData, verbose_name=_(
        "miner data"), on_delete=models.CASCADE, primary_key=True)
    total_diesel = models.DecimalField(
        _("jumlah diesel"), max_digits=15, decimal_places=2)
    total_electric = models.DecimalField(
        _("jumlah elektrik"), max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "bahan tenaga"
        verbose_name_plural = "bahan tenaga"

    def __str__(self):
        return f"{self.miner_data}"


class OperatingRecord(models.Model):
    miner_data = models.OneToOneField(QuarryMinerData, verbose_name=_(
        "miner data"), on_delete=models.CASCADE, primary_key=True)
    operating_hours = models.IntegerField(_("jam operasi sehari"))
    operating_days = models.IntegerField(_("bilangan hari operasi"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "rekod operasi"
        verbose_name_plural = "rekod operasi"

    def __str__(self):
        return f"{self.miner_data}"


class Royalties(models.Model):
    miner_data = models.OneToOneField(QuarryMinerData, verbose_name=_(
        "miner data"), on_delete=models.CASCADE, primary_key=True)
    royalties = models.DecimalField(
        _("royalti"), max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "royalti"
        verbose_name_plural = "royalti"

    def __str__(self):
        return f"{self.miner_data}"


class Other(models.Model):
    miner_data = models.ForeignKey(QuarryMinerData, verbose_name=_(
        "miner data"), on_delete=models.CASCADE, related_name='others')
    title = models.CharField(_("tajuk"), max_length=255, blank=True)
    comment = models.TextField(_("komen"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "lain-lain"
        verbose_name_plural = "lain-lain"

    def __str__(self):
        return f'{self.miner_data} ({self.pk})'


class QuarryDataApproval(models.Model):
    miner_data = models.ForeignKey(QuarryMinerData, verbose_name=_(
        "miner data"), on_delete=models.CASCADE, related_name='approvals')
    requestor = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "requestor"), on_delete=models.CASCADE, related_name='quarry_requested')
    state_inspector = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "state inspector"), on_delete=models.SET_NULL, related_name='quarry_state_inspected', null=True, blank=True)
    state_comment = models.TextField(_("state comment"), blank=True)
    state_approved = models.BooleanField(
        _("state approved"), null=True, blank=True)
    admin_inspector = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "admin inspector"), on_delete=models.SET_NULL, related_name='quarry_admin_inspected', null=True, blank=True)
    admin_comment = models.TextField(_("admin comment"), blank=True)
    admin_approved = models.BooleanField(
        _("admin approved"), null=True, blank=True)
    hq_inspector = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "hq inspector"), on_delete=models.SET_NULL, related_name='quarry_hq_inspected', null=True, blank=True)
    hq_comment = models.TextField(_("hq comment"), blank=True)
    hq_approved = models.BooleanField(_("hq approved"), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.miner_data} ({self.pk})'
