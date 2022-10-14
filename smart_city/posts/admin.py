from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import News, Article, Question, Theme, QuestionReview, NewsReview, ArticleReview, Tags, Notification, \
    UserUploadImage
from django.utils.safestring import mark_safe


class NewsReviewAdmin(admin.TabularInline):
    model = NewsReview
    extra = 0


class NewsAdmin(admin.ModelAdmin):
    inlines = [NewsReviewAdmin]


class ArticleReviewAdmin(admin.TabularInline):
    model = ArticleReview
    extra = 0


class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleReviewAdmin]


# class ImageInline(admin.TabularInline):
#     model = ImageQuestion
#     readonly_fields = ('render_image',)
#
#     def render_image(self, obj):
#         return mark_safe("""<img src="%s" width="80" height="80"/>""" % obj.image.url)


class QuestionReviewAdmin(admin.TabularInline):
    model = QuestionReview
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionReviewAdmin]


admin.site.register(News, NewsAdmin)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ["title", "is_active"]


@admin.register(Question)
class NewsAdmin(admin.ModelAdmin):
    list_display = ["title", "is_active"]


@admin.register(Article)
class NewsAdmin(admin.ModelAdmin):
    list_display = ["title", "is_active"]


admin.site.register(Notification)
admin.site.register(UserUploadImage)


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    pass


@admin.register(Theme)
class ThemesAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 20
