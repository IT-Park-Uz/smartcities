from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView

# Facebook
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

# GitHub
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView

# Google
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

# Connect with SocialLogin
from dj_rest_auth.registration.views import SocialConnectView

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    # callback_url = 'CALLBACK_URL_YOU_SET_ON_GITHUB'
    # client_class = OAuth2Client

class GitHubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    # callback_url = 'CALLBACK_URL_YOU_SET_ON_GITHUB'
    client_class = OAuth2Client

class GoogleLogin(SocialLoginView): # if you want to use Authorization Code Grant, use this
    adapter_class = GoogleOAuth2Adapter
    # callback_url = 'CALLBACK_URL_YOU_SET_ON_GOOGLE'
    client_class = OAuth2Client

# Connect to Social
class FacebookConnect(SocialConnectView):
    adapter_class = FacebookOAuth2Adapter
    # callback_url = 'CALLBACK_URL_YOU_SET_ON_GITHUB'
    # client_class = OAuth2Client

class GithubConnect(SocialConnectView):
    adapter_class = GitHubOAuth2Adapter
    # callback_url = 'CALLBACK_URL_YOU_SET_ON_GITHUB'
    client_class = OAuth2Client

class GoogleConnect(SocialConnectView):
    adapter_class = GoogleOAuth2Adapter
    # callback_url = 'CALLBACK_URL_YOU_SET_ON_GITHUB'
    client_class = OAuth2Client
