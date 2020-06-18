from rest_framework import serializers

from .models import (
    TranslationMemory,
    TMContent,
    GlossaryType,
    Glossary,
    GlossaryContent,
    Project,
    File,
    Sentence,
)


class TranslationMemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TranslationMemory
        fields = ('id', 'name', 'description', 'src_lang', 'tar_lang', 'user')


class TMContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TMContent
        fields = ('id', 'src_sentence', 'tar_sentence', 'translation_memory')        


class GlossaryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlossaryType
        fields = ('id', 'name', 'description', 'user')


class GlossarySerializer(serializers.ModelSerializer):
    # gloss_type = GlossaryTypeSerializer(many=True)
    class Meta:
        model = Glossary
        fields = ('id', 'name', 'description', 'src_lang', 'tar_lang', 'user', 'gloss_type')


class GlossaryContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlossaryContent
        fields = ('id', 'src_phrase', 'tar_phrase', 'glossary')


class ProjectSerializer(serializers.ModelSerializer):
    # translation_memory = TranslationMemorySerializer(many=True)
    # glossary = GlossarySerializer(many=True)

    class Meta:
        model = Project        
        fields = ('id', 'name', 'user', 'src_lang', 'tar_lang', 'translate_service', 'translation_memory', 'glossary')


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"



class SentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentence
        fields = "__all__"

