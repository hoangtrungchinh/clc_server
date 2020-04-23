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
)

admin.site.register(TranslationMemory)
admin.site.register(TMContent)
admin.site.register(GlossaryType)
admin.site.register(Glossary)
admin.site.register(GlossaryContent)
admin.site.register(Project)
admin.site.register(File)

