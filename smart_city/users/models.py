from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    name = CharField(max_length=100)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

class Person(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Person',null=True,blank=True)
    county = models.CharField(max_length=50,null=True,blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    job_adress = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-id']

    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return ''

    def __str__(self):
        return f"{self.id}| {self.user.username}"

class Organization(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='Organization',null=True,blank=True)
    county = models.CharField(max_length=50,null=True,blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    employee_count = models.IntegerField()
    bio = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-id']

    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return ''

    def __str__(self):
        return f"{self.id}| {self.user.username} | {self.organization_name[:20]}"
