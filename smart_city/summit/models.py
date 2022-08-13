from django.db import models

class Summit(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    location = models.CharField(max_length=150)
    start_time = models.DateField()
    end_time = models.DateField()

    def __str__(self):
        return self.title[:20]

class Programs(models.Model):
    summit = models.ForeignKey(Summit, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title[:20]


class Participant(models.Model):

    category =(
        (1,"Tashrif buyuruvchi"),
        (2,"Ishtirokchi"),
        (3,"Spiker"),
        (4,"OAV")
    )
    summit = models.OneToOneField(Summit, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    oragnization = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    category = models.CharField(max_length=100, choices=category)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.summit.title[:20]} | {self.full_name}"
