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
    File
)


class TranslationMemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TranslationMemory
        fields = ('id', 'name', 'description', 'src_lang', 'tar_lang', 'user')

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


class GlossaryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlossaryType
        fields = ('id', 'name', 'description', 'user')


class GlossarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Glossary
        fields = ('id', 'name', 'description', 'src_lang', 'tar_lang', 'gloss_type', 'user')

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

class FileWithChildSerializer(serializers.ModelSerializer):
    sentence_set = SentenceSerializer(many=True, read_only=True)
    class Meta:
        model = File
        fields = ('id', 'file', 'project', 'confirm', 'sentence_set')
