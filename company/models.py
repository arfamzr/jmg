from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy, reverse


# Create your models here.

class Company(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name=_("user"), on_delete=models.CASCADE)
    # company_id = models.IntegerFields(_("id"))
    company_name = models.CharField(_("nama syarikat"), max_length=255)
    company_address = models.CharField(_("alamat syarikat"), max_length=255)
    company_state = models.CharField(_("negeri"), max_length=50)
    company_phone = models.CharField(_("no phone"), max_length=50)
    company_fax = models.CharField(_("no fax"), max_length=50)
    company_email = models.CharField(_("emel"), max_length=255)

    class Meta:
        verbose_name = "syarikat"
        verbose_name_plural = "syarikat"

    def __str__(self):
        return f"{self.company}"

    def get_update_url(self):
        return reverse("company:update", kwargs={"pk": self.pk})
    
    def get_detail_url(self):
        return reverse("company:detail", kwargs={"pk": self.pk})
