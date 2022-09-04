from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import News, Article, Question, Theme, ImageQuestion, QuestionReview, NewsReview, ArticleReview, Tags, \
    UserLikedNews, UserLikedArticles, UserLikedQuestions
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


class ImageInline(admin.TabularInline):
    model = ImageQuestion
    extra = 0
    readonly_fields = ('render_image',)

    def render_image(self, obj):
        return mark_safe("""<img src="%s" width="80" height="80"/>""" % obj.image.url)


class QuestionReviewAdmin(admin.TabularInline):
    model = QuestionReview
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ImageInline, QuestionReviewAdmin]


admin.site.register(News, NewsAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(UserLikedNews)
admin.site.register(UserLikedArticles)
admin.site.register(UserLikedQuestions)


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    pass


@admin.register(Theme)
class ThemesAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 20
