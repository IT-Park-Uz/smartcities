from django.shortcuts import render
from rest_framework import viewsets, status
from .serializer import *

class SummitView(viewsets.ModelViewSet):
    queryset = Summit.objects.all()
    serializer_class = SummitSerializer

class ProgramsView(viewsets.ModelViewSet):
    queryset = Programs.objects.all()
    serializer_class = ProgramsSerializer

class ParticipantView(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
