from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_("email"), unique=True)

    @property
    def is_industry(self):
        return self.is_active and (self.is_superuser or self.groups.filter(name="Industry").exists())

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
    image = models.ImageField(
        _("image"), upload_to='uploads/profile_images/%Y/%m/%d/', blank=True)
    state = models.CharField(_("state"), max_length=3, choices=STATE_CHOICES)

    def __str__(self):
        return f'{self.user}'

class UserUpdate(models.Model):
    user = models.OneToOneField(User, verbose_name=_(
        "user"), on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(_("user name"), max_length=255)
    first_name = models.CharField(
        _("first name"), max_length=255)
    last_name = models.CharField(_("last name"), max_length=255)
    email = models.CharField(_("email"), max_length=15)

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "user"

    def __str__(self):
        return self.user

    def get_update_url(self):
        return reverse("account:update", kwargs={"pk": self.pk})