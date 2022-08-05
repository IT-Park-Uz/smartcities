from django.contrib import admin
from .models import News, Article, Question, Theme, ImageQuestion, QuestionReview, NewsReview, ArticleReview
from django.utils.safestring import mark_safe



class NewsReviewAdmin(admin.TabularInline):
    model = NewsReview
    extra = 1
class NewsAdmin(admin.ModelAdmin):
    inlines = [NewsReviewAdmin]
class ArticleReviewAdmin(admin.TabularInline):
    model = ArticleReview
    extra = 1
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleReviewAdmin]
class ImageInline(admin.TabularInline):
    model = ImageQuestion
    extra = 1
    readonly_fields = ('render_image',)
    def render_image(self, obj):
        return mark_safe("""<img src="%s" width="80" height="80"/>""" % obj.image.url)

class QuestionReviewAdmin(admin.TabularInline):
    model = QuestionReview
    extra = 1
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ImageInline, QuestionReviewAdmin]

admin.site.register(News, NewsAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Theme)
