from django.urls import path
from idegovuz.views import IdEgovUzAdapter, oauth2_login

from smart_city.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
)
from .views import (FacebookLogin, GitHubLogin,GoogleLogin, FacebookConnect, GithubConnect)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),

    # Social Login
    path('dj-rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('dj-rest-auth/github/', GitHubLogin.as_view(), name='github_login'),
    path('dj-rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('dj-rest-auth/idegovuz/', oauth2_login, name='google_login'),

    # Social connect
    path('dj-rest-auth/facebook/connect/', FacebookConnect.as_view(), name='fb_connect'),
    path('dj-rest-auth/github/connect/', GithubConnect.as_view(), name='github_connect'),
    path('dj-rest-auth/google/connect/', GoogleLogin.as_view(), name='google_connect'),
]
