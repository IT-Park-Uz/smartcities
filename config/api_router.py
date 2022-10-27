from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from smart_city.posts.views import (NewsApiView, ArticleApiView, QuestionApiView, UserNewsView,
                                    UserArticleView, UserQuestionView, TagsApiView, ThemeApiView, SearchNewsView,
                                    SearchArticleView, SearchQuestionView, NewsReviewView, ArticleReviewView,
                                    QuestionReviewView, NotificationApiView,
                                    LikeNewsView, ReadNewsView, LikeArticlesView, ReadArticlesView, LikeQuestionsView,
                                    ReadQuestionsView, ThemeGroupNewsView, ThemeGroupArticlesView,
                                    ThemeGroupQuestionsView, UserSavedCollectionsView, UserUploadImageView)
from smart_city.social_auth.views import GoogleSocialAuthView, FacebookSocialAuthView, TwitterSocialAuthView
from smart_city.users.api.views import UserViewSet

from idegovuz.views import IdEgovUzAdapter, oauth2_login

from smart_city.users.views import (
    RegisterAPIView, VerifyCodeView, LogoutView, ResetPasswordView,
)
from smart_city.users.views import (PasswordChangeView)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register('news', NewsApiView, basename='news')
router.register('article', ArticleApiView, basename='article')
router.register('question', QuestionApiView, basename='question')
router.register('tags', TagsApiView, basename='tags')
router.register('theme', ThemeApiView, basename='theme')

router.register('theme-gr-news', ThemeGroupNewsView, basename='theme-gr-news')
router.register('theme-gr-qs', ThemeGroupQuestionsView, basename='theme-gr-qs')
router.register('theme-gr-ar', ThemeGroupArticlesView, basename='theme-gr-ar')

# sidebar routes
router.register('n-like', LikeNewsView, basename='n-like')
router.register('n-read', ReadNewsView, basename='n-read')
router.register('a-like', LikeArticlesView, basename='a-like')
router.register('a-read', ReadArticlesView, basename='a-read')
router.register('q-like', LikeQuestionsView, basename='q-like')
router.register('q-read', ReadQuestionsView, basename='q-read')

router.register('news-comment', NewsReviewView, basename='news-comment')
router.register('articles-comment', ArticleReviewView, basename='articles-comment')
router.register('questions-comment', QuestionReviewView, basename='questions-comment')

router.register('search-news', SearchNewsView, basename='search-news')
router.register('search-articles', SearchArticleView, basename='search-articles')
router.register('search-questions', SearchQuestionView, basename='search-questions')

router.register('news-history', UserNewsView, basename='news-history')
router.register('articles-history', UserArticleView, basename='articles-history')
router.register('questions-history', UserQuestionView, basename='questions-history')

router.register('notifications', NotificationApiView, basename='notifications')
router.register('user-uploads', UserUploadImageView, basename='user-uploads')

router.register('password_reset', ResetPasswordView, basename='password_reset')

app_name = "api"
urlpatterns = router.urls
urlpatterns += [

]

# TODO: USERS urls
urlpatterns += [
    path('register/', RegisterAPIView.as_view(), name="register"),
    path('verify/', VerifyCodeView.as_view(), name="verify"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    # path('password/reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('saved/', UserSavedCollectionsView.as_view(), name='saved'),

    # SOCIAL AUTH
    path('social/google', GoogleSocialAuthView.as_view()),
    path('social/linked', FacebookSocialAuthView.as_view()),
    path('social/github', TwitterSocialAuthView.as_view()),

    # Social Login
    # path('social/facebook/', FacebookLogin.as_view(), name='fb_login'),
    # path('social/github/', GitHubLogin.as_view(), name='github_login'),
    # path('social/google/', GoogleLogin.as_view(), name='google_login'),
    # path('social/idegovuz/', oauth2_login, name='google_login'),

    # Social connect
    # path('social/facebook/connect/', FacebookConnect.as_view(), name='fb_connect'),
    # path('social/github/connect/', GithubConnect.as_view(), name='github_connect'),
    # path('social/google/connect/', GoogleLogin.as_view(), name='google_connect'),
]
