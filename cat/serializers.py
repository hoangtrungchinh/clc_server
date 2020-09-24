from rest_framework import serializers
from django.conf import settings
import ntpath
from rest_framework import fields
from .models import (
    TranslationMemory,
    TMContent,
    GlossaryType,
    Glossary,
    GlossaryContent,
    Project,
    File,
    Sentence,
    File,
    Corpus,
    CorpusContent
)

from rest_framework.validators import UniqueTogetherValidator


class TranslationMemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TranslationMemory
        fields = ('id', 'name', 'description', 'src_lang', 'tar_lang', 'user')
        validators = [
            UniqueTogetherValidator(
                queryset=TranslationMemory.objects.all(),
                message='This name is exist',
                fields=['name', 'user']
            )
        ]

    def validate(self, data):
        if data['src_lang'] == data['tar_lang']:
            raise serializers.ValidationError("Source and Target language must be different")
        return data


class TMContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TMContent
        fields = ('id', 'src_sentence', 'tar_sentence', 'translation_memory')        

class ImportTMSerializer(serializers.Serializer):
    tm_id = serializers.IntegerField()
    tm_file = serializers.FileField()

class ImportGlossarySerializer(serializers.Serializer):
    glossary_id = serializers.IntegerField()
    glossary_file = serializers.FileField()

class ImportCorpusSerializer(serializers.Serializer):
    corpus_id = serializers.IntegerField()
    corpus_file = serializers.FileField()

class MachineTranslateSerializer(serializers.Serializer):
    src_lang = serializers.ChoiceField(settings.LANGUAGE)
    tar_lang = serializers.ChoiceField(settings.LANGUAGE)
    sentence = serializers.CharField()


class GlossaryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlossaryType
        fields = ('id', 'name', 'description', 'user')
        validators = [
            UniqueTogetherValidator(
                queryset=GlossaryType.objects.all(),
                message='This name is exist',
                fields=['name', 'user']
            )
        ]



class GlossarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Glossary
        fields = ('id', 'name', 'description', 'src_lang', 'tar_lang', 'gloss_type', 'user')
        validators = [
            UniqueTogetherValidator(
                queryset=Glossary.objects.all(),
                message='This name is exist',
                fields=['name', 'user']
            )
        ]

    def validate(self, data):
        if data['src_lang'] == data['tar_lang']:
            raise serializers.ValidationError("Source and Target language must be different")
        return data    

class GlossaryWithChildSerializer(serializers.ModelSerializer):
    gloss_type = GlossaryTypeSerializer(many=True, read_only=True)
    class Meta:
        model = Glossary
        fields = ('id', 'name', 'description', 'src_lang', 'tar_lang', 'gloss_type', 'user')

class GlossaryContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlossaryContent
        fields = ('id', 'src_phrase', 'tar_phrase', 'glossary')

class CustomMultipleChoiceField(fields.MultipleChoiceField):
    def to_representation(self, value):
        return list(super().to_representation(value))
        
class ProjectSerializer(serializers.ModelSerializer):
    translate_service = CustomMultipleChoiceField(choices=settings.TRANSLATION_SERVICE)
    class Meta:
        model = Project        
        fields = ('id', 'name', 'user', 'src_lang', 'tar_lang', 'translate_service', 'searchable_translation_memory', 'glossary', 'writable_translation_memory')
        validators = [
            UniqueTogetherValidator(
                queryset=Project.objects.all(),
                message='This name is exist',
                fields=['name', 'user']
            )
        ]

        
class ProjectWithChildSerializer(serializers.ModelSerializer):
    translate_service = CustomMultipleChoiceField(choices=settings.TRANSLATION_SERVICE)
    searchable_translation_memory = TranslationMemorySerializer(many=True, read_only=True)
    writable_translation_memory = TranslationMemorySerializer(read_only=True)
    glossary = GlossarySerializer(many=True, read_only=True)
    class Meta:
        model = Project        
        fields = ('id', 'name', 'user', 'src_lang', 'tar_lang', 'translate_service', 'searchable_translation_memory', 'glossary', 'writable_translation_memory')

class FileSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()
    def get_filename(self, obj):
        return ntpath.basename(obj.file.name)

    class Meta:
        model = File
        fields = ('id','file', 'project', 'confirm', 'filename')

class SentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentence
        fields = ('id', 'src_str','tar_str','score','is_confirmed','tag','file')

class SentenceWithIDSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    class Meta:
        model = Sentence
        fields = ('id', 'src_str','tar_str','score','is_confirmed','tag','file')

class FileWithChildSerializer(serializers.ModelSerializer):
    sentence_set = SentenceSerializer(many=True, read_only=True)
    class Meta:
        model = File
        fields = ('id', 'file', 'project', 'confirm', 'sentence_set')

class CorpusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corpus
        fields = ("id", "name", "language", "user", "description")

class CorpusContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorpusContent
        fields = ("id", "corpus", "phrase")

