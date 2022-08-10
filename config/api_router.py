from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from smart_city.posts.views import (NewsApiView, ArticleApiView, QuestionApiView, UserNewsView,
                                    UserArticleView, UserQuestionView,
                                    ImageQuestionApiView, TagsApiView, ThemeApiView, SearchNewsView)
from smart_city.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register('news', NewsApiView, basename='news')
router.register('search-news', SearchNewsView, basename='search-news')
router.register('article', ArticleApiView, basename='article')
router.register('question', QuestionApiView, basename='question')
router.register('question-image', ImageQuestionApiView, basename='question-image')
router.register('tags', TagsApiView, basename='tags')
router.register('theme', ThemeApiView, basename='theme')

router.register('news-history', UserNewsView, basename='news-history')
router.register('article-history', UserArticleView, basename='article-history')
router.register('question-history', UserQuestionView, basename='question-history')

app_name = "api"
urlpatterns = router.urls
urlpatterns += [
]
