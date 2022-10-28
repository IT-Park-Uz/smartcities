import requests
from django.conf import settings
from rest_framework import serializers
from . import google, facebook, twitterhelper
from .register import register_social_user
from rest_framework.exceptions import AuthenticationFailed


class FacebookSocialAuthSerializer(serializers.Serializer):
    """Handles serialization of facebook related data"""
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = facebook.Facebook.validate(auth_token)

        try:
            user_id = user_data['id']
            email = user_data['email']
            name = user_data['name']
            provider = 'facebook'
            return register_social_user(
                provider=provider,
                user_id=user_id,
                email=email,
                name=name
            )
        except Exception as identifier:
            raise serializers.ValidationError(
                'The token  is invalid or expired. Please login again.'
            )


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )
        if user_data['aud'] != settings.GOOGLE_CLIENT_ID:
            raise AuthenticationFailed('oops, who are you?')
        user_id = user_data['sub']
        email = user_data['email']
        first_name = user_data['given_name']
        last_name = user_data['family_name']
        name = user_data['name']
        provider = 'google'
        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name, first_name=first_name, last_name=last_name)


class LinkedInSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token_for_linkedin_obtain_access_token):
        # Getting an access token
        access_token = requests.post(
            'https://www.linkedin.com/oauth/v2/accessToken',
            data={
                'client_id': '7854iw2a91d5ru',
                'client_secret': 'uIOjYkbST9m2CXzd',
                'redirect_uri': 'https://hub.smartcities.uz/linkedin',
                'code': auth_token_for_linkedin_obtain_access_token,
                'grant_type': 'authorization_code'
            }
        ).json()
        if access_token.get('error') is not None:
            raise serializers.ValidationError({'detail': access_token.get('error')})
        access_token = access_token['access_token']
        user_sso_data = requests.get(
            'https://api.linkedin.com/v2/me',
            headers={
                'Authorization': f"Bearer {access_token}"
            }
        ).json()
        try:
            user_email = requests.get(
                'https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))',
                headers={
                    'Authorization': f"Bearer {access_token}"
                }
            ).json()
            if user_email.get('serviceErrorCode') is not None:
                raise serializers.ValidationError({'detail': user_email.get('serviceErrorCode')})
            user_email = user_email['elements'][0]['handle~'].get('emailAddress')
            if user_email is None:
                raise serializers.ValidationError({'detail': 'Your LinkedIn account has not an email or SSO has bad configuration'})
            return register_social_user(
                provider='linkedin',
                user_id=user_sso_data['id'],
                email=user_email,
                name=user_sso_data['id'],
                first_name=user_sso_data.get('localizedFirstName'),
                last_name=user_sso_data.get('localizedLastName')
            )
        except (IndexError, KeyError) as e:
            raise serializers.ValidationError({'detail': 'Your LinkedIn account has not an email or SSO has bad configuration'})


class TwitterAuthSerializer(serializers.Serializer):
    """Handles serialization of twitter related data"""
    access_token_key = serializers.CharField()
    access_token_secret = serializers.CharField()

    def validate(self, attrs):

        access_token_key = attrs.get('access_token_key')
        access_token_secret = attrs.get('access_token_secret')

        user_info = twitterhelper.TwitterAuthTokenVerification.validate_twitter_auth_tokens(
            access_token_key, access_token_secret)

        try:
            user_id = user_info['id_str']
            email = user_info['email']
            name = user_info['name']
            provider = 'twitter'
        except:
            raise serializers.ValidationError(
                'The tokens are invalid or expired. Please login again.'
            )

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name)
