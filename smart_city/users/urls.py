from django.urls import path
from idegovuz.views import IdEgovUzAdapter, oauth2_login

from smart_city.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view, RegisterAPIView, VerifyCodeView,
)
from .views import (FacebookLogin, GitHubLogin,GoogleLogin, FacebookConnect, GithubConnect)

app_name = "users"
urlpatterns = [
    path('register/',RegisterAPIView.as_view(),name="register"),
    path('verify/',VerifyCodeView.as_view(),name="verify"),

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
