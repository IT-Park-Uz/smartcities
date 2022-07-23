from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    image = models.ImageField(upload_to='Users', null=True, blank=True)
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name=_('Organization'), related_name='users')

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


class Organization(models.Model):
    organization_name = models.CharField(max_length=50, verbose_name=_('Organization'))
    image = models.ImageField(upload_to='Organization', null=True, blank=True, verbose_name=_('Image'))
    bio = models.TextField(null=True, blank=True, verbose_name=_('Bio'))
    is_active = models.BooleanField(default=False, verbose_name=_('Is Active'))

    class Meta:
        ordering = ['-id']

    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return ''

    def __str__(self):
        return f"{self.id}| {self.organization_name[:20]}"
