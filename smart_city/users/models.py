from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import random


class User(AbstractUser):
    image = models.ImageField(upload_to='Users', null=True, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    organization_name = models.CharField(max_length=70, verbose_name=_('Organization'), null=True, blank=True)
    work_name = models.CharField(_('work name'), max_length=255, null=True, blank=True)
    bio = models.TextField(null=True, blank=True, verbose_name=_('Bio'))
    is_verified = models.BooleanField(_('is verified'), default=False)
    gender = models.BooleanField(_('gender'), default=True)
    country = models.CharField(_('country'), max_length=255, null=True)
    country_code = models.CharField(_('country code'), max_length=255, null=True)
    phone = models.CharField(_('phone'), max_length=255, null=True)
    birthday_date = models.DateField(null=True)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})



class Code(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=6,null=True, blank=True)

    def __str__(self):
        return f"{self.number}"

    def save(self, *args, **kwargs):
        number_list = [x for x in range(10)]
        code_items = ''
        for i in range(6):
            num = random.choice(number_list)
            code_items += str(num)
        self.number = code_items
        super().save(*args, **kwargs)


class ChangedPassword(models.Model):
    user = models.ForeignKey(User, related_name='changed_password_users', on_delete=models.CASCADE)
    password = models.CharField(max_length=10)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
