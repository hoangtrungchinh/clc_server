from rest_framework import serializers

from .models import TranslationMemory

class TranslationMemorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TranslationMemory
        fields = ('id', 'src', 'tar')
