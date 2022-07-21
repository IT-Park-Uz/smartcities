from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from smart_city.users.models import User
from mptt.models import MPTTModel, TreeForeignKey


class News(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    theme = models.ForeignKey('Theme', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='News', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tags')

    class Meta:
        ordering = ['-id']

    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return ''

    def __str__(self):
        return f"{self.id} | {self.title[:20]}"


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    theme = models.ForeignKey('Theme', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='Article', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return ''

    def __str__(self):
        return f"{self.id} | {self.title[:20]}"


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    theme = models.ForeignKey('Theme', on_delete=models.SET_NULL, null=True)
    type = models.ForeignKey('Type_Question', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.id} | {self.title[:20]}"


class Type_Question(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class ImageQuestion(models.Model):
    name = models.CharField(max_length=255)
    product = models.ForeignKey(Question, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='QuestionImages')
    default = models.BooleanField(default=False)

class Tags(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.id} | {self.name}"


class Theme(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, related_name='children')
    name = models.CharField(max_length=50, unique=True)

    class MPTTMeta:
        order_insertion_by = ['-id']

    def __str__(self):
        return f"{self.id} | {self.name}"


class Review(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self',on_delete=models.CASCADE)

