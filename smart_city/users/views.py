from dj_rest_auth.serializers import PasswordChangeSerializer
from dj_rest_auth.views import sensitive_post_parameters_m
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from allauth.account.models import EmailAddress

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
from rest_framework import generics, status, viewsets
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

from smart_city.users.api.serializers import RegisterSerializer, CodeSerializer
from smart_city.users.models import Code
from smart_city.users.serializer import LogOutSerializer
from smart_city.users.utils import send_email

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


class GoogleLogin(SocialLoginView):  # if you want to use Authorization Code Grant, use this
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


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        check = self.check_user_verify(request)
        if serializer.is_valid(raise_exception=True):
            if check:
                serializer.save()
            else:
                return Response({'message':'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
            code, created = Code.objects.get_or_create(user_id=serializer.data['id'])
            code.save()
            send_email({'to_email': serializer.data['email'], 'code': code.number})
            # Todo: send the code by email to user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def check_user_verify(self, request):
        try:
            email = request.data.get('email')
        except:
            return True
        if not EmailAddress.objects.filter(email=email).first():
            user = User.objects.filter(email=email)
            user.delete()
            return True
        else:
            return False


class VerifyCodeView(generics.GenericAPIView):
    serializer_class = CodeSerializer
    permission_classes = (AllowAny,)
    queryset = Code.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            num = Code.objects.filter(user_id=int(serializer.data['user'])).first()
            if not num:
                return Response({'error': 'code not found'}, status=status.HTTP_400_BAD_REQUEST)
            if str(num.number) == str(serializer.data['number']):
                user = User.objects.filter(id=int(serializer.data['user'])).first()
                EmailAddress.objects.create(user=user, email=user.email, primary=True, verified=True)
                token = self.get_tokens_for_user(user)
                login(request, user)
                return Response({'Message': 'Successfully activated', 'token': token}, status=status.HTTP_200_OK)
            return Response({'Message': 'Code is not match'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {'refresh': str(refresh), 'access': str(refresh.access_token)}


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogOutSerializer

    def post(self, request, *args, **kwargs):
        serializer = LogOutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            token = RefreshToken(serializer.data['refresh'])
        except:
            return Response({'message': "Token is blacklisted"}, status=status.HTTP_400_BAD_REQUEST)
        logout(request)
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)


class PasswordChangeView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordChangeSerializer
    throttle_scope = 'dj_rest_auth'

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            if serializer.data.get("new_password1") == serializer.data.get("new_password2"):
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
                }
                return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
