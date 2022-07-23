from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    image = models.ImageField(upload_to='Users', null=True, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    organization_name = models.CharField(max_length=70, verbose_name=_('Organization'), null=True, blank=True)
    work_name = models.CharField(_('work name'), max_length=255, null=True, blank=True)
    bio = models.TextField(null=True, blank=True, verbose_name=_('Bio'))

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

