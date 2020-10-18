from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from account.models import User, Profile
from quarry.models import QuarryMinerData, YEAR_CHOICES, current_year, Quarry


class Mine(models.Model):
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
    main_rock_type = models.CharField(
        _("jenis batuan utama"), max_length=255, choices=Quarry.TYPES_OF_ROCK)
    side_rock_type = models.CharField(
        _("jenis batuan sampingan"), max_length=255, blank=True, choices=Quarry.TYPES_OF_ROCK)
    status = models.BooleanField(_("status"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "lombong"
        verbose_name_plural = "lombong"

    def __str__(self):
        return f'{self.location}, {self.mukim}, {self.district}, {self.get_state_display()}'

    def get_absolute_url(self):
        return reverse("mine:state_admin:detail", kwargs={"pk": self.pk})

    def get_state_absolute_url(self):
        return reverse("mine:state:detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("mine:state_admin:update", kwargs={"pk": self.pk})

    def get_toggle_active_url(self):
        return reverse("mine:state_admin:toggle_active", kwargs={"pk": self.pk})

    def get_add_miner_url(self):
        return reverse("mine:state_admin:add_miner", kwargs={"pk": self.pk})


class MineMiner(models.Model):
    miner = models.ForeignKey(User, verbose_name=_(
        "pengusaha"), on_delete=models.CASCADE, related_name='mines_mined')
    mine = models.ForeignKey(Mine, verbose_name=_(
        "kuari"), on_delete=models.CASCADE, related_name="miners")
    add_by = models.ForeignKey(User, verbose_name=_(
        "add by"), on_delete=models.SET_NULL, related_name='mine_miners_added', null=True)
    lot_number = models.CharField(_("no lot"), max_length=255)
    latitude = models.DecimalField(
        _("latitude"), max_digits=15, decimal_places=4)
    longitude = models.DecimalField(
        _("longitude"), max_digits=15, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "pengusaha lombong"
        verbose_name_plural = "pengusaha lombong"

    def __str__(self):
        return f'{self.miner} ({self.mine})'

    def get_delete_url(self):
        return reverse("mine:state_admin:mine_remove_miner", kwargs={"pk": self.pk})

    def get_add_report_url(self):
        return reverse("mine:add_report", kwargs={"pk": self.pk})


class MineMinerData(models.Model):
    miner = models.ForeignKey(MineMiner, verbose_name=_(
        "pengusaha"), on_delete=models.SET_NULL, related_name='data', null=True)
    mine = models.ForeignKey(Mine, verbose_name=_(
        "lombong"), on_delete=models.SET_NULL, related_name='miner_data', null=True)
    state = models.CharField(_("negeri"), max_length=3,
                             choices=Profile.STATE_CHOICES)
    month = models.PositiveIntegerField(
        _("bulan"), choices=QuarryMinerData.MONTH_CHOICES)
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
        return reverse("mine:miner_data", kwargs={"pk": self.pk})

    def get_state_absolute_url(self):
        return reverse("mine:state:miner_data", kwargs={"pk": self.pk})

    def get_state_admin_absolute_url(self):
        return reverse("mine:state_admin:miner_data", kwargs={"pk": self.pk})

    def get_edit_url(self):
        return reverse("mine:statistic_edit", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("mine:miner_data_delete", kwargs={"pk": self.pk})

    def get_last_approval(self):
        return self.approvals.last()


class Statistic(models.Model):
    miner_data = models.OneToOneField(MineMinerData, verbose_name=_(
        "miner data"), on_delete=models.CASCADE, primary_key=True)
    minerals_quantity = models.DecimalField(
        _("kuantiti_mineral"), max_digits=15, decimal_places=2)
    final_stock_last_month = models.DecimalField(
        _("stok akhir bulan lalu"), max_digits=15, decimal_places=2)
    mine_production = models.DecimalField(
        _("pengeluaran lombong"), max_digits=15, decimal_places=2)
    total_minerals = models.DecimalField(
        _("jumlah mineral"), max_digits=15, decimal_places=2)
    submission_buyers = models.DecimalField(
        _("penyerahan kepada pembeli"), max_digits=15, decimal_places=2)
    final_stock_this_month = models.DecimalField(
        _("stok akhir bulan ini"), max_digits=15, decimal_places=2)
    average_grade = models.CharField(_("gred hitung panjang"), max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "perangkaan"
        verbose_name_plural = "perangkaan"

    def __str__(self):
        return f"{self.miner_data}"


class LocalOperator(models.Model):
    miner_data = models.OneToOneField(MineMinerData, verbose_name=_(
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
    miner_data = models.OneToOneField(MineMinerData, verbose_name=_(
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
    miner_data = models.OneToOneField(MineMinerData, verbose_name=_(
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
    miner_data = models.OneToOneField(MineMinerData, verbose_name=_(
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
    miner_data = models.OneToOneField(MineMinerData, verbose_name=_(
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
    miner_data = models.OneToOneField(MineMinerData, verbose_name=_(
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


class EnergySupply(models.Model):
    miner_data = models.OneToOneField(MineMinerData, verbose_name=_(
        "miner data"), on_delete=models.CASCADE, primary_key=True)
    total_diesel = models.DecimalField(
        _("jumlah diesel"), max_digits=15, decimal_places=2)
    total_electric = models.DecimalField(
        _("jumlah elektrik"), max_digits=15, decimal_places=2)
    total_explosive = models.DecimalField(
        _("jumlah bahan letupan"), max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "bahan tenaga"
        verbose_name_plural = "bahan tenaga"

    def __str__(self):
        return f"{self.miner_data}"


class OperatingRecord(models.Model):
    miner_data = models.OneToOneField(MineMinerData, verbose_name=_(
        "miner data"), on_delete=models.CASCADE, primary_key=True)
    average_mine_depth = models.DecimalField(
        _("dalam lombong hitung panjang"), max_digits=15, decimal_places=2)
    deepest_mine = models.DecimalField(
        _("ukuran lombong terdalam"), max_digits=15, decimal_places=2)
    shallowest_mine = models.DecimalField(
        _("ukuran lombong tercetek"), max_digits=15, decimal_places=2)
    material_discarded = models.DecimalField(
        _("bahan beban dibuang"), max_digits=15, decimal_places=4)
    ore_mined = models.DecimalField(
        _("bahan berbijih dilombong"), max_digits=15, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "rekod operasi"
        verbose_name_plural = "rekod operasi"

    def __str__(self):
        return f"{self.miner_data}"


class MineDataApproval(models.Model):
    miner_data = models.ForeignKey(MineMinerData, verbose_name=_(
        "miner data"), related_name='approvals', on_delete=models.CASCADE)
    requestor = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "requestor"), on_delete=models.CASCADE, related_name='mine_requested')
    state_inspector = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "state inspector"), on_delete=models.SET_NULL, related_name='mine_state_inspected', null=True, blank=True)
    state_comment = models.TextField(_("state comment"), blank=True)
    state_approved = models.BooleanField(
        _("state approved"), null=True, blank=True)
    admin_inspector = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "admin inspector"), on_delete=models.SET_NULL, related_name='mine_admin_inspected', null=True, blank=True)
    admin_comment = models.TextField(_("admin comment"), blank=True)
    admin_approved = models.BooleanField(
        _("admin approved"), null=True, blank=True)
    hq_inspector = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "hq inspector"), on_delete=models.SET_NULL, related_name='mine_hq_inspected', null=True, blank=True)
    hq_comment = models.TextField(_("hq comment"), blank=True)
    hq_approved = models.BooleanField(_("hq approved"), null=True, blank=True)

    def __str__(self):
        return f'{self.miner_data} ({self.pk})'
