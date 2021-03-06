from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_("email"), unique=True)

    @property
    def is_manager(self):
        return self.is_active and (self.is_superuser or self.groups.filter(name="Manager").exists())

    @property
    def is_jmg_state(self):
        return self.is_active and (self.is_superuser or self.groups.filter(name='JMG State').exists())

    @property
    def is_jmg_state_admin(self):
        return self.is_active and (self.is_superuser or self.groups.filter(name='JMG State Admin').exists())

    @property
    def is_jmg_hq(self):
        return self.is_active and (self.is_superuser or self.groups.filter(name='JMG HQ').exists())

    @property
    def is_super_admin(self):
        return self.is_active and (self.is_superuser or self.groups.filter(name='Super Admin').exists())

    def get_hq_absolute_url(self):
        return reverse("account:super_admin:hq_detail", kwargs={"pk": self.pk})

    def get_hq_update_url(self):
        return reverse("account:super_admin:hq_update", kwargs={"pk": self.pk})

    def get_hq_toggle_active_url(self):
        return reverse("account:super_admin:hq_toggle_active", kwargs={"pk": self.pk})

    def get_hq_reset_password_url(self):
        return reverse("account:super_admin:hq_update_password", kwargs={"pk": self.pk})

    def get_admin_absolute_url(self):
        return reverse("account:super_admin:admin_detail", kwargs={"pk": self.pk})

    def get_admin_update_url(self):
        return reverse("account:super_admin:admin_update", kwargs={"pk": self.pk})

    def get_admin_reset_password_url(self):
        return reverse("account:super_admin:admin_update_password", kwargs={"pk": self.pk})

    # def get_absolute_url(self):
    #     return reverse("account:state_admin:user_detail", kwargs={"pk": self.pk})

    def get_state_absolute_url(self):
        return reverse("account:state:user_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("account:state_admin:user_update", kwargs={"pk": self.pk})

    # def get_reset_password_url(self):
    #     return reverse("account:state_admin:user_update_password", kwargs={"pk": self.pk})

    def get_jmg_update_url(self):
        return reverse("account:state_admin:state_update", kwargs={"pk": self.pk})

    # def get_toggle_active_url(self):
    #     return reverse("account:state_admin:user_toggle_active", kwargs={"pk": self.pk})

    def get_quarry_list_url(self):
        return reverse("quarry:state_admin:user_quarry_list", kwargs={"pk": self.pk})

    def get_mine_list_url(self):
        return reverse("mine:state_admin:user_mine_list", kwargs={"pk": self.pk})

    def get_state_quarry_list_url(self):
        return reverse("quarry:state:user_quarry_list", kwargs={"pk": self.pk})

    def get_state_mine_list_url(self):
        return reverse("mine:state:user_mine_list", kwargs={"pk": self.pk})

    ############################################################

    # state admin - state
    def state_admin_get_state_update_url(self):
        return reverse("account:state_admin:state_update", kwargs={"pk": self.pk})

    def state_admin_get_toggle_active_url(self):
        return reverse("account:state_admin:state_toggle_active", kwargs={"pk": self.pk})

    def state_admin_get_state_update_state_url(self):
        return reverse("account:state_admin:state_update_state", kwargs={"pk": self.pk})

    # super admin - hq
    def super_admin_get_hq_update_url(self):
        return reverse("account:super_admin:hq_update", kwargs={"pk": self.pk})

    def super_admin_get_hq_toggle_active_url(self):
        return reverse("account:super_admin:hq_toggle_active", kwargs={"pk": self.pk})

    # super admin - state admin
    def super_admin_get_state_admin_update_url(self):
        return reverse("account:super_admin:state_admin_update", kwargs={"pk": self.pk})

    def super_admin_get_state_admin_toggle_active_url(self):
        return reverse("account:super_admin:state_admin_toggle_active", kwargs={"pk": self.pk})

    def super_admin_get_state_admin_update_state_url(self):
        return reverse("account:super_admin:state_admin_update_state", kwargs={"pk": self.pk})


class Profile(models.Model):
    JOHOR = 'JHR'
    KEDAH = 'KDH'
    KELANTAN = 'KTN'
    MALACCA = 'MLK'
    N_SEMBILAN = 'NSN'
    PAHANG = 'PHG'
    PENANG = 'PNG'
    PERAK = 'PRK'
    PERLIS = 'PLS'
    SABAH = 'SBH'
    SARAWAK = 'SWK'
    SELANGOR = 'SGR'
    TERENGGANU = 'TRG'
    K_LUMPUR = 'KUL'
    LABUAN = 'LBN'
    PUTRAJAYA = 'PJY'
    STATE_CHOICES = [
        (JOHOR, 'Johor'),
        (KEDAH, 'Kedah'),
        (KELANTAN, 'Kelantan'),
        (MALACCA, 'Melaka'),
        (N_SEMBILAN, 'Negeri Sembilan'),
        (PAHANG, 'Pahang'),
        (PENANG, 'Pulau Pinang'),
        (PERAK, 'Perak'),
        (PERLIS, 'Perlis'),
        (SABAH, 'Sabah'),
        (SARAWAK, 'Sarawak'),
        (SELANGOR, 'Selangor'),
        (TERENGGANU, 'Terengganu'),
        (K_LUMPUR, 'Kuala Lumpur'),
        (LABUAN, 'Labuan'),
        (PUTRAJAYA, 'Putrajaya'),
    ]

    user = models.OneToOneField(User, verbose_name=_(
        "user"), on_delete=models.CASCADE, primary_key=True)
    ic_number = models.CharField(_("No Kad Pengenalan"), max_length=25)
    address1 = models.CharField(
        _("alamat (No Rumah, Nama Jalan)"), max_length=255)
    address2 = models.CharField(
        _("alamat (Daerah)"), max_length=255, blank=True)
    address3 = models.CharField(
        _("alamat (Poskod, Negeri)"), max_length=255, blank=True)
    image = models.ImageField(
        _("image"), upload_to='uploads/profile_images/%Y/%m/%d/', blank=True)
    state = models.CharField(_("state"), max_length=3, choices=STATE_CHOICES)

    def __str__(self):
        return f'{self.user}'

    def get_update_url(self):
        return reverse("account:update", kwargs={"pk": self.pk})
