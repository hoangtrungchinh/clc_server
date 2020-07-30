from django.contrib import admin

# Register your models here.
from .models import (
    TranslationMemory,
    TMContent,
    GlossaryType,
    Glossary,
    GlossaryContent,
    Project,
    File,
    Sentence,
    Corpus,
    CorpusContent,
)


class TranslationMemoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "src_lang", "tar_lang", "user")


class TMContentAdmin(admin.ModelAdmin):
    list_display = ("id", "src_sentence", "tar_sentence", "translation_memory")
    

class GlossaryTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "user")


class GlossaryAdmin(admin.ModelAdmin):
    list_display = ("id", "description", "name", "src_lang", "tar_lang", "user", "get_gloss_types")


class GlossaryContentAdmin(admin.ModelAdmin):
    list_display = ("id", "src_phrase", "tar_phrase", "glossary")


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user", "src_lang", "tar_lang", "translate_service", "list_glossary", "list_translation_memory")


class FileAdmin(admin.ModelAdmin):
    list_display = ("id", "file", "project", "confirm",)


class SentenceAdmin(admin.ModelAdmin):
    list_display = ("id", "file", "src_str", "tar_str", "score", "is_confirmed", "tag")


class CorpusAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "language", "user", "description")


class CorpusContentAdmin(admin.ModelAdmin):
    list_display = ("id", "phrase", "corpus")




admin.site.register(TranslationMemory, TranslationMemoryAdmin)
admin.site.register(TMContent, TMContentAdmin)
admin.site.register(GlossaryType, GlossaryTypeAdmin)
admin.site.register(Glossary, GlossaryAdmin)
admin.site.register(GlossaryContent, GlossaryContentAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Sentence, SentenceAdmin)
admin.site.register(Corpus, CorpusAdmin)
admin.site.register(CorpusContent, CorpusContentAdmin)

