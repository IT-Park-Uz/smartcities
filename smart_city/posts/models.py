from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

from smart_city.users.models import User
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _


class News(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    theme = models.ForeignKey('Theme', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    subtitle = RichTextUploadingField(null=True)
    image = models.ImageField(upload_to='News/%y/%m/%d', null=True, blank=True)
    description = RichTextUploadingField()
    view_count = models.IntegerField(default=0)
    user_liked = models.ManyToManyField(User, related_name="user_liked_n", null=True, blank=True)
    saved_collections = models.ManyToManyField(User, related_name="user_saved_n", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tags', null=True, blank=True)
    is_delete = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=False)
    extra_data = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name = _("Новость")
        verbose_name_plural = _("Новости")

    @property
    def like_count(self):
        return self.user_liked.count()

    @property
    def saved_count(self):
        return self.saved_collections.count()

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
    subtitle = RichTextUploadingField(null=True)
    image = models.ImageField(upload_to='Article/%y/%m/%d', null=True, blank=True)
    description = RichTextUploadingField()
    view_count = models.IntegerField(default=0)
    user_liked = models.ManyToManyField(User, related_name="user_liked_a", null=True, blank=True)
    saved_collections = models.ManyToManyField(User, related_name="user_saved_a", null=True)
    tags = models.ManyToManyField('Tags', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']
        verbose_name = _("Статья")
        verbose_name_plural = _("Статьи")

    @property
    def like_count(self):
        return self.user_liked.count()

    @property
    def saved_count(self):
        return self.saved_collections.count()

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
    image = models.ImageField(upload_to='Question/%y/%m/%d', null=True, blank=True)
    type = models.IntegerField(default=Type_Question.EASY, choices=Type_Question.choices)
    title = models.CharField(max_length=200)
    subtitle = RichTextUploadingField(null=True)
    description = RichTextUploadingField()
    view_count = models.IntegerField(default=0)
    user_liked = models.ManyToManyField(User, related_name="user_liked_q", null=True, blank=True)
    saved_collections = models.ManyToManyField(User, related_name="user_saved_q", null=True, blank=True)
    tags = models.ManyToManyField('Tags', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']
        verbose_name = _("Вопрос")
        verbose_name_plural = _("Вопросы")

    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return ''

    @property
    def like_count(self):
        return self.user_liked.count()

    @property
    def saved_count(self):
        return self.saved_collections.count()

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


class Tags(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=False)  # TODO:new part

    def __str__(self):
        return f"{self.id} | {self.name}"

    class Meta:
        verbose_name = _("Тег")
        verbose_name_plural = _("Теги")


class Theme(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    name = models.CharField("Name in english", max_length=50, unique=True)
    name_uz = models.CharField("Name in uzbek", max_length=50, null=True)
    name_tu = models.CharField("Name in turkish", max_length=50, null=True)
    name_az = models.CharField("Name in azerbaijanian", max_length=50, null=True)
    name_kz = models.CharField("Name in kazakhian", max_length=50, null=True)
    name_kr = models.CharField("Name in kyrgyzian", max_length=50, null=True)
    icon = models.FileField("Icon", upload_to='Themes/%y/%m/%d', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['-id']

    def __str__(self):
        return f"{self.id} | {self.name}"

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")


class Notification(models.Model):
    user_read = models.ManyToManyField(User)
    title = models.CharField(max_length=255)
    description = RichTextUploadingField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} | {self.title[:20]}"

class UserUploadImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="UserUploadImage")

    def __str__(self):
        return self.user.username
