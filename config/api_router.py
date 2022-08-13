from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from smart_city.posts.views import (NewsApiView, ArticleApiView, QuestionApiView, UserNewsView,
                                    UserArticleView, UserQuestionView,
                                    ImageQuestionApiView, TagsApiView, ThemeApiView, SearchNewsView, SearchArticleView,
                                    SearchQuestionView, NewsReviewView, ArticleReviewView, QuestionReviewView)
from smart_city.summit.views import (SummitView, ProgramsView, ParticipantView)
from smart_city.users.api.views import UserViewSet

from idegovuz.views import IdEgovUzAdapter, oauth2_login

from smart_city.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view, RegisterAPIView, VerifyCodeView, LogoutView,
)
from smart_city.users.views import (FacebookLogin, GitHubLogin,GoogleLogin, FacebookConnect, GithubConnect, PasswordChangeView)

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

router.register('new-comment', NewsReviewView, basename='new-comment')
router.register('article-comment', ArticleReviewView, basename='article-comment')
router.register('question-comment', QuestionReviewView, basename='question-comment')

router.register('search-news', SearchNewsView, basename='search-news')
router.register('search-articles', SearchArticleView, basename='search-articles')
router.register('search-question', SearchQuestionView, basename='search-question')


router.register('news-history', UserNewsView, basename='news-history')
router.register('article-history', UserArticleView, basename='article-history')
router.register('question-history', UserQuestionView, basename='question-history')

# SUMMITS
router.register('summit', SummitView, basename='summit')
router.register('program', ProgramsView, basename='program')
router.register('participant', ParticipantView, basename='participant')


app_name = "api"
urlpatterns = router.urls
urlpatterns += [

]

# TODO: USERS urls
urlpatterns += [
    path('register/',RegisterAPIView.as_view(),name="register"),
    path('verify/',VerifyCodeView.as_view(),name="verify"),
    path('logout/',LogoutView.as_view(),name="logout"),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('password/change/',PasswordChangeView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),

    # Social Login
    path('social/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('social/github/', GitHubLogin.as_view(), name='github_login'),
    path('social/google/', GoogleLogin.as_view(), name='google_login'),
    path('social/idegovuz/', oauth2_login, name='google_login'),

    # Social connect
    path('social/facebook/connect/', FacebookConnect.as_view(), name='fb_connect'),
    path('social/github/connect/', GithubConnect.as_view(), name='github_connect'),
    path('social/google/connect/', GoogleLogin.as_view(), name='google_connect'),
]
