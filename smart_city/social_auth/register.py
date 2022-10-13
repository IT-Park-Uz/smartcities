from allauth.account.models import EmailAddress
from django.conf import settings
from django.contrib.auth import authenticate
import random
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from smart_city.users.api.serializers import RegisterSerializer

User = get_user_model()


def generate_username(name):
    username = "".join(name.split(' ')).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


def register_social_user(provider, user_id, email, name, first_name, last_name):
    # if provider=='facebook':
    #     password = settings.FACEBOOK_SOCIAL_SECRET
    # elif provider=='google':
    #     password = settings.GOOGLE_CLIENT_SECRET

    email_check = User.objects.filter(email=email).first()
    if email_check is not None:
        registered_user = authenticate(
            username=email_check.username, password=user_id)
        if registered_user:
            refresh = RefreshToken.for_user(registered_user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + provider)
    else:
        user = {
            'username': generate_username(name), 'email': email,
            'first_name': first_name, 'last_name': last_name,
            'password': user_id}
        serializer = RegisterSerializer(data=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = User.objects.filter(id=int(serializer.data['id'])).first()
            user.is_verified = True
            user.save()
            EmailAddress.objects.create(user=user, email=user.email, primary=True, verified=True)
        new_user = authenticate(
            username=user.username, password=user_id)
        if new_user:
            refresh = RefreshToken.for_user(user)

            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        else:
            raise AuthenticationFailed(
                detail='Please login again.')
