from django.shortcuts import render

from rest_framework import viewsets
from .serializers import ClcSerializer
from .models import clc


class ClcViewSet(viewsets.ModelViewSet):
    queryset = clc.objects.all().order_by('tar')
    serializer_class = ClcSerializer


