from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from smart_city.posts.views import (NewsApiView, ArticleApiView, QuestionApiView, UserNewsView,
                                    UserArticleView, UserQuestionView,
                                    ImageQuestionApiView, TagsApiView, ThemeApiView, ReviewApiView)
from smart_city.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register('news', NewsApiView, basename='news')
router.register('article', ArticleApiView, basename='article')
router.register('question', QuestionApiView, basename='question')
router.register('question-image', ImageQuestionApiView, basename='question-image')
router.register('tags', TagsApiView, basename='tags')
router.register('theme', ThemeApiView, basename='theme')
router.register('review', ReviewApiView, basename='review')

app_name = "api"
urlpatterns = router.urls
urlpatterns += [
    path('news-history/', UserNewsView.as_view(), name='news-history'),
    path('article-history/', UserArticleView.as_view(), name='article-history'),
    path('question-history/', UserQuestionView.as_view(), name='question-history'),
]
