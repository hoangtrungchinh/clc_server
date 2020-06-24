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
)


class TranslationMemoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "src_lang", "tar_lang", "user")


class TMContentAdmin(admin.ModelAdmin):
    list_display = ("src_sentence", "tar_sentence", "translation_memory")
    

class GlossaryTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "user")


class GlossaryAdmin(admin.ModelAdmin):
    list_display = ("description", "name", "src_lang", "tar_lang", "user", "get_gloss_types")


class GlossaryContentAdmin(admin.ModelAdmin):
    list_display = ("src_phrase", "tar_phrase", "glossary")


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "src_lang", "tar_lang", "translate_service", "list_glossary", "list_translation_memory")


class FileAdmin(admin.ModelAdmin):
    list_display = ("file", "project", "confirm",)


class SentenceAdmin(admin.ModelAdmin):
    list_display = ("file", "src_str", "tar_str", "score", "is_confirmed", "tag")




admin.site.register(TranslationMemory, TranslationMemoryAdmin)
admin.site.register(TMContent, TMContentAdmin)
admin.site.register(GlossaryType, GlossaryTypeAdmin)
admin.site.register(Glossary, GlossaryAdmin)
admin.site.register(GlossaryContent, GlossaryContentAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Sentence, SentenceAdmin)

