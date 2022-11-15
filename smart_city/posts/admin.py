from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import News, Article, Question, Theme, QuestionReview, NewsReview, ArticleReview, Tags, Notification, \
    UserUploadImage
from django.utils.safestring import mark_safe


class NewsReviewAdmin(admin.TabularInline):
    model = NewsReview
    extra = 0


class ArticleReviewAdmin(admin.TabularInline):
    model = ArticleReview
    extra = 0


class QuestionReviewAdmin(admin.TabularInline):
    model = QuestionReview
    extra = 0

# class ImageInline(admin.TabularInline):
#     model = ImageQuestion
#     readonly_fields = ('render_image',)
#
#     def render_image(self, obj):
#         return mark_safe("""<img src="%s" width="80" height="80"/>""" % obj.image.url)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    inlines = [NewsReviewAdmin]
    list_display = ["title", "is_active"]
    raw_id_fields = ["user", "theme", "tags", "user_liked", "saved_collections"]
    search_fields = ["user__first_name", "user__last_name", "title"]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionReviewAdmin]
    list_display = ["title", "is_active"]
    raw_id_fields = ["user", "theme"]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleReviewAdmin]
    list_display = ["title", "is_active"]
    raw_id_fields = ["user", "theme"]


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
