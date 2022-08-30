from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.db.models.fields import related
import os

from smart_city.users.models import User
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _


class News(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    theme = models.ForeignKey('Theme', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='News/%y/%m/%d', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tags', blank=True)
    is_delete = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']
        verbose_name = _("Новость")
        verbose_name_plural = _("Новости")

    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return ''

    def __str__(self):
        return f"{self.id} | {self.title[:20]}"


class NewsReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    comment = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.id} | {self.user.username}"

    class Meta:
        verbose_name = _("Комментарии к новостью")
        verbose_name_plural = _("Комментарии к новостям")


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    theme = models.ForeignKey('Theme', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='Article/%y/%m/%d', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    tags = models.ManyToManyField('Tags', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']
        verbose_name = _("Статья")
        verbose_name_plural = _("Статьи")

    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return ''

    def __str__(self):
        return f"{self.id} | {self.title[:20]}"


class ArticleReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.id} | {self.user.username}"

    class Meta:
        verbose_name = _("Комментарии к статье")
        verbose_name_plural = _("Комментарии к статьям")


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
    tags = models.ManyToManyField('Tags', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']
        verbose_name = _("Вопрос")
        verbose_name_plural = _("Вопросы")

    def __str__(self):
        return f"{self.id} | {self.title[:20]}"


class QuestionReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    comment = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.id} | {self.user.username}"


class ImageQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_images', null=True,
                                 blank=True)
    image = models.ImageField(upload_to='QuestionImages/%y/%m/%d', null=True, blank=True)
    default = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Изображения вопроса")
        verbose_name_plural = _("Изображении вопросов")

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

    class Meta:
        verbose_name = _("Тег")
        verbose_name_plural = _("Теги")


class Theme(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['-id']

    def __str__(self):
        return f"{self.id} | {self.name}"

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")
