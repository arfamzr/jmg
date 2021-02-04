from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from account.models import User, Profile
from quarry.models import Data, YEAR_CHOICES, current_year


class Choices:
    BAUXITE = 'BAUXITE'
    TINORE = 'TIN ORE'
    IRONORE = 'IRON ORE'
    ANTIMONY = 'ANTIMONY'
    COAL = 'COAL'
    DIMENSIONSTONE = 'DIMENSION STONE'
    FELDSPAR = 'FELDSPAR'
    GALENA = 'GALENA'
    LIMESTONE = 'BATU KAPUR'
    KAOLIN = 'KAOLIN'
    CUPRUM = 'CUPRUM'
    BALLCLAY = 'BALL CLAY'
    MANGANESE = 'MANGANESE'
    SHALE = 'SHALE'
    MICA = 'MICA'
    SILVER = 'SILVER'
    SILICASAND = 'SILICA SAND'
    TUNGSTEN = 'TUNGSTEN'
    GOLD = 'GOLD'
    GRAPHITE = 'GRAPHITE'
    TYPES_OF_MINERAL = [
        (BAUXITE, _('Bauksite/Bauksit')),
        (TINORE, _('Tin Ore/Bijih Timah')),
        (IRONORE, _('Iron Ore/Bijih Besi')),
        (ANTIMONY, _('Antimony/Antimoni')),
        (COAL, _('Coal/Arang Batu')),
        (DIMENSIONSTONE, _('Dimension Stone/Batu Dimensi')),
        (FELDSPAR, _('Feldspar/Felspar')),
        (GALENA, _('Galena/Galena')),
        (LIMESTONE, _('Limestone/Batu Kapur')),
        (KAOLIN, _('Kaolin')),
        (CUPRUM, _('Kuprum')),
        (BALLCLAY, _('Ball Clay/Lempung Bebola')),
        (MANGANESE, _('Manganese/Mangan')),
        (MICA, _('Mica/Mika')),
        (SILVER, _('Silver/Perak')),
        (SILICASAND, _('Silica Sand/Pasir Silika')),
        (TUNGSTEN, _('Tungsten')),
        (GOLD, _('Gold/Emas')),
        (GRAPHITE, _('Graphite/Grafit')),
    ]

    KG = 'KG'
    M3 = 'M3'
    GRAM = 'GRAM'
    TAN = 'TAN'

    UNIT_CHOICES = [
        (KG, _('Kilogram')),
        (M3, _('Meter Persegi')),
        (GRAM, _('Gram')),
        (TAN, _('Tan')),

    ]


class ProcessFactory(models.Model):
    name = models.CharField(_("nama"), max_length=255)
    license_no = models.CharField(
        _("no. lesen memproses mineral"), max_length=255)
    state = models.CharField(_("negeri"), max_length=3,
                             choices=Profile.STATE_CHOICES)
    status = models.BooleanField(_("status"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "kilang proses"
        verbose_name_plural = "kilang proses"

    def __str__(self):
        return self.name

    def get_update_url(self):
        return reverse("mineral:state_admin:process_factory_update", kwargs={"pk": self.pk})

    def get_toggle_active_url(self):
        return reverse("mineral:state_admin:process_factory_toggle_active", kwargs={"pk": self.pk})

    def get_manager_create_url(self):
        return reverse("mineral:state_admin:manager_create", kwargs={"pk": self.pk})


class ProcessManager(models.Model):
    user = models.OneToOneField(User, verbose_name=_(
        "user"), on_delete=models.CASCADE, primary_key=True)
    factory = models.OneToOneField(ProcessFactory, verbose_name=_(
        "kilang"), on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "pengurus lesen memproses"
        verbose_name_plural = "pengurus lesen memproses"

    def __str__(self):
        return f'{self.user}'

    def get_update_url(self):
        return reverse("mineral:state_admin:manager_update", kwargs={"pk": self.pk})

    def get_toggle_active_url(self):
        return reverse("mineral:state_admin:manager_toggle_active", kwargs={"pk": self.pk})


class ProcessData(models.Model):
    manager = models.ForeignKey(ProcessManager, verbose_name=_(
        "pengurus"), on_delete=models.SET_NULL, related_name='process_data', null=True)
    factory = models.ForeignKey(ProcessFactory, verbose_name=_(
        "kilang"), on_delete=models.SET_NULL, related_name='data', null=True)
    state = models.CharField(_("negeri"), max_length=3,
                             choices=Profile.STATE_CHOICES)
    month = models.PositiveIntegerField(
        _("bulan"), choices=Data.MONTH_CHOICES)
    year = models.PositiveIntegerField(
        _("tahun"), choices=YEAR_CHOICES, default=current_year)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "data lesen memproses"
        verbose_name_plural = "data lesen memproses"

    def __str__(self):
        return f'{self.factory} - {self.pk}'

    def get_absolute_url(self):
        return reverse("mineral:data_detail", kwargs={"pk": self.pk})

    def get_state_absolute_url(self):
        return reverse("mineral:state:data_detail", kwargs={"pk": self.pk})

    def get_state_admin_absolute_url(self):
        return reverse("mineral:state_admin:data_detail", kwargs={"pk": self.pk})

    def get_state_admin_success_url(self):
        return reverse("mineral:state_admin:data_success_detail", kwargs={"pk": self.pk})

    # def get_hq_success_url(self):
    #     return reverse("mineral:hq:data_success_detail", kwargs={"pk": self.pk})

    # def get_hq_absolute_url(self):
    #     return reverse("mineral:hq:data_detail", kwargs={"pk": self.pk})

    def get_edit_url(self):
        return reverse("mineral:process_statistic_edit", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("mineral:data_delete", kwargs={"pk": self.pk})

    def get_last_approval(self):
        return self.approvals.last()


class ProcessStatistic(models.Model):
    data = models.ForeignKey(ProcessData, verbose_name=_(
        "data"), on_delete=models.CASCADE, related_name="statistics")
    mineral_type = models.CharField(
        _("jenis mineral"), max_length=255, choices=Choices.TYPES_OF_MINERAL)
    quantity_unit = models.CharField(
        _("unit kuantiti"), max_length=255, choices=Choices.UNIT_CHOICES, default=Choices.TAN)
    initial_stock = models.DecimalField(
        _("stok awal bulan"), max_digits=15, decimal_places=2)
    external_sources = models.DecimalField(
        _("pembelian dari punca luar"), max_digits=15, decimal_places=2)
    production = models.DecimalField(
        _("pengeluaran"), max_digits=15, decimal_places=2)
    total = models.DecimalField(
        _("jumlah"), max_digits=15, decimal_places=2)
    sold = models.DecimalField(
        _("penjualan"), max_digits=15, decimal_places=2)
    final_stock = models.DecimalField(
        _("stock akhir bulan"), max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "perangkaan lesen proses"
        verbose_name_plural = "perangkaan lesen proses"

    def __str__(self):
        return f"{self.get_mineral_type_display()} - {self.data}"

    def get_absolute_url(self):
        return reverse("mineral:process_statistic_detail", kwargs={"pk": self.pk})

    def get_edit_url(self):
        return reverse("mineral:process_statistic_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("mineral:process_statistic_delete", kwargs={"pk": self.pk})


class ProcessSubmission(models.Model):
    data = models.ForeignKey(ProcessData, verbose_name=_(
        "data"), on_delete=models.CASCADE, related_name="submission")
    mineral_type = models.CharField(
        _("jenis mineral"), max_length=255, choices=Choices.TYPES_OF_MINERAL)
    quantity_unit = models.CharField(
        _("unit kuantiti"), max_length=255, choices=Choices.UNIT_CHOICES, default=Choices.TAN)
    quantity = models.DecimalField(
        _("kuantiti"), max_digits=15, decimal_places=2)
    buyer = models.CharField(_("pembeli"), max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "statistic lesen process"
        verbose_name_plural = "statistic lesen process"

    def __str__(self):
        return f"{self.get_mineral_type_display()} - {self.data}"

    def get_absolute_url(self):
        return reverse("mineral:process_submission_detail", kwargs={"pk": self.pk})

    def get_edit_url(self):
        return reverse("mineral:process_submission_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("mineral:process_submission_delete", kwargs={"pk": self.pk})


class LocalOperator(models.Model):
    data = models.OneToOneField(ProcessData, verbose_name=_(
        "data"), on_delete=models.CASCADE, primary_key=True)
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
    total_male = models.IntegerField(_("jumlah lelaki"))
    total_female = models.IntegerField(_("jumlah perempuan"))
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
        return f"{self.data}"


class ForeignOperator(models.Model):
    data = models.OneToOneField(ProcessData, verbose_name=_(
        "data"), on_delete=models.CASCADE, primary_key=True)
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
        return f"{self.data}"


class LocalContractor(models.Model):
    data = models.OneToOneField(ProcessData, verbose_name=_(
        "data"), on_delete=models.CASCADE, primary_key=True)
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
        return f"{self.data}"


class ForeignContractor(models.Model):
    data = models.OneToOneField(ProcessData, verbose_name=_(
        "data"), on_delete=models.CASCADE, primary_key=True)
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
        return f"{self.data}"


class InternalCombustionMachinery(models.Model):
    data = models.OneToOneField(ProcessData, verbose_name=_(
        "data"), on_delete=models.CASCADE, primary_key=True)
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
        return f"{self.data}"


class ElectricMachinery(models.Model):
    data = models.OneToOneField(ProcessData, verbose_name=_(
        "data"), on_delete=models.CASCADE, primary_key=True)
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
        return f"{self.data}"


class EnergySupply(models.Model):
    data = models.OneToOneField(ProcessData, verbose_name=_(
        "data"), on_delete=models.CASCADE, primary_key=True)
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
        return f"{self.data}"


class OperatingRecord(models.Model):
    data = models.OneToOneField(ProcessData, verbose_name=_(
        "data"), on_delete=models.CASCADE, primary_key=True)
    operating_hours = models.IntegerField(_("jam operasi sehari"))
    operating_days = models.IntegerField(_("bilangan hari operasi"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "rekod operasi"
        verbose_name_plural = "rekod operasi"

    def __str__(self):
        return f"{self.data}"


class Other(models.Model):
    data = models.ForeignKey(ProcessData, verbose_name=_(
        "data"), on_delete=models.CASCADE, related_name='others')
    title = models.CharField(_("tajuk"), max_length=255, blank=True)
    comment = models.TextField(_("komen"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "lain-lain"
        verbose_name_plural = "lain-lain"

    def __str__(self):
        return f'{self.data} ({self.pk})'


class Approval(models.Model):
    data = models.ForeignKey(ProcessData, verbose_name=_(
        "data"), on_delete=models.CASCADE, related_name='approvals')
    requestor = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "requestor"), on_delete=models.CASCADE, related_name='process_requested')
    state_inspector = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "state inspector"), on_delete=models.SET_NULL, related_name='process_state_inspected', null=True, blank=True)
    state_comment = models.TextField(_("state comment"), blank=True)
    state_approved = models.BooleanField(
        _("state approved"), null=True, blank=True)
    admin_inspector = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "admin inspector"), on_delete=models.SET_NULL, related_name='process_admin_inspected', null=True, blank=True)
    admin_comment = models.TextField(_("admin comment"), blank=True)
    admin_approved = models.BooleanField(
        _("admin approved"), null=True, blank=True)
    hq_inspector = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "hq inspector"), on_delete=models.SET_NULL, related_name='process_hq_inspected', null=True, blank=True)
    hq_comment = models.TextField(_("hq comment"), blank=True)
    hq_approved = models.BooleanField(_("hq approved"), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.data} ({self.pk})'
