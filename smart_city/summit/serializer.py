from rest_framework import serializers
from .models import (Summit, Programs, Participant)

class SummitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Summit
        fields = '__all__'

class ProgramsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programs
        fields = '__all__'

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'
