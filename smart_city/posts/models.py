from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from smart_city.users.models import User
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _


class News(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    theme = models.ForeignKey('Theme', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='News', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tags', null=True, blank=True)
    is_delete = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

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
    tags = models.ManyToManyField('Tags', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

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


class Type_Question(models.IntegerChoices):
    EASY = 1, _('EASY')
    MIDDLE = 2, _('MIDDLE')
    HARD = 3, _('HARD')


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    theme = models.ForeignKey('Theme', on_delete=models.SET_NULL, null=True)
    type = models.IntegerField(default=Type_Question.EASY, choices=Type_Question.choices)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    tags = models.ManyToManyField('Tags', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.id} | {self.title[:20]}"


class ImageQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='QuestionImages')
    default = models.BooleanField(default=True)

    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return ''

    def __str__(self):
        return f"{self.id}"


class Tags(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.id} | {self.name}"


class Theme(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['-id']

    def __str__(self):
        return f"{self.id} | {self.name}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE)
