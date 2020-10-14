from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy, reverse

from account.models import User, Profile


class Company(models.Model):
    name = models.CharField(_("nama syarikat"), max_length=255)
    address1 = models.CharField(_("alamat"), max_length=255)
    address2 = models.CharField(
        _("alamat (line 2)"), max_length=255, blank=True)
    address3 = models.CharField(
        _("alamat (line 3)"), max_length=255, blank=True)
    state = models.CharField(_("negeri"), max_length=3,
                             choices=Profile.STATE_CHOICES)
    phone = models.CharField(_("no phone"), max_length=50)
    fax = models.CharField(_("no fax"), max_length=50)
    email = models.CharField(_("emel"), max_length=255)
    status = models.BooleanField(_("status"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "syarikat"
        verbose_name_plural = "syarikat"

    def __str__(self):
        return self.name

    def get_update_url(self):
        return reverse("company:state_admin:update", kwargs={"pk": self.pk})

    def get_absolute_url(self):
        return reverse("company:state_admin:detail", kwargs={"pk": self.pk})

    def get_add_employee_url(self):
        return reverse("company:state_admin:add_employee", kwargs={"pk": self.pk})


class Employee(models.Model):
    user = models.OneToOneField(
        User, verbose_name=_("user"), on_delete=models.CASCADE)
    company = models.ForeignKey(Company, verbose_name=_(
        "syarikat"), on_delete=models.SET_NULL, related_name='employees', null=True)
    add_by = models.ForeignKey(User, verbose_name=_(
        "add by"), on_delete=models.SET_NULL, related_name='employees_added', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "pekerja"
        verbose_name_plural = "pekerja"

    def __str__(self):
        return f'{self.user} - {self.company}'
