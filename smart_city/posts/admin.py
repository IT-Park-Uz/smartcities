from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import News, Article, Question, Theme, QuestionReview, NewsReview, ArticleReview, Tags, Notification, \
    UserUploadImage
from django.utils.safestring import mark_safe
from django.forms.fields import BooleanField


class NewsReviewAdmin(admin.TabularInline):
    model = NewsReview
    readonly_fields = ("comment",)
    extra = 0


class ArticleReviewAdmin(admin.TabularInline):
    model = ArticleReview
    readonly_fields = ("comment",)
    extra = 0


class QuestionReviewAdmin(admin.TabularInline):
    model = QuestionReview
    extra = 0
    readonly_fields = ("comment",)


# class ImageInline(admin.TabularInline):
#     model = ImageQuestion
#     readonly_fields = ('render_image',)
#
#     def render_image(self, obj):
#         return mark_safe("""<img src="%s" width="80" height="80"/>""" % obj.image.url)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    inlines = [NewsReviewAdmin]
    list_display = ["title", "is_active", "user"]
    raw_id_fields = ["user", "theme", "tags", "user_liked", "saved_collections"]
    search_fields = ["user__first_name", "user__last_name", "title"]
    list_editable = ['is_active']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        if not is_superuser:
            for i in form.base_fields.values():
                i.disabled = True if type(i) != BooleanField else False

        return form


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionReviewAdmin]
    list_display = ["title", "is_active"]
    raw_id_fields = ["user", "theme"]

    list_editable = ['is_active']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        if not is_superuser:
            for i in form.base_fields.values():
                i.disabled = True if type(i) != BooleanField else False

        return form


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleReviewAdmin]
    list_display = ["title", "is_active"]
    raw_id_fields = ["user", "theme"]

    list_editable = ['is_active']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        if not is_superuser:
            for i in form.base_fields.values():
                i.disabled = True if type(i) != BooleanField else False

        return form


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    pass


@admin.register(UserUploadImage)
class UserUploadImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active"]


@admin.register(Theme)
class ThemesAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 20
