from rest_framework import serializers

from .models import clc

class ClcSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = clc
        fields = ('src', 'tar')
