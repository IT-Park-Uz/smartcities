from rest_framework import serializers


class LogOutSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length=255)
