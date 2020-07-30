from django.db import models
from django.contrib.auth.models import User
import os
import sys
from django.conf import settings
from multiselectfield import MultiSelectField

sys.path.append(os.path.join(settings.BASE_DIR,'preprocessing_python'))
from preprocessor import *

class TranslationMemory(models.Model):
    name = models.TextField()
    description = models.TextField()
    src_lang = models.CharField(choices=settings.LANGUAGE, max_length=2)
    tar_lang = models.CharField(choices=settings.LANGUAGE, max_length=2)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('name', 'user',)   

    def __str__(self):
        # return sys.path
        return str(self.id) + " | " + self.name + " | " + self.src_lang+ " | " + self.tar_lang

    def get_user_id(self):
        return self.user.id
        

class TMContent(models.Model):
    src_sentence = models.TextField()
    tar_sentence = models.TextField()
    translation_memory = models.ForeignKey(TranslationMemory, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('src_sentence', 'tar_sentence', 'translation_memory')   
        
    def __str__(self):
        return str(self.id) + " | " + self.src_sentence + " | " + self.tar_sentence
        

class GlossaryType(models.Model):
    name = models.TextField()
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('name', 'user',)   

    def __str__(self):
        return str(self.id) + " | " + self.name


class Glossary(models.Model):
    name = models.TextField()
    description = models.TextField()
    src_lang = models.CharField(choices=settings.LANGUAGE, max_length=2)
    tar_lang = models.CharField(choices=settings.LANGUAGE, max_length=2)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    gloss_type = models.ManyToManyField(GlossaryType)

    class Meta:
        unique_together = ('name', 'user',)   

    def __str__(self):
        return str(self.id) + " | " + self.src_lang + " | " + self.tar_lang       

    def get_user_id(self):
        return self.user.id

    def get_gloss_types(self):
        return ", ".join([p.name for p in self.gloss_type.all()])

    
class GlossaryContent(models.Model):
    src_phrase = models.TextField()
    tar_phrase = models.TextField()
    glossary = models.ForeignKey(Glossary, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('src_phrase', 'tar_phrase','glossary')    
    def __str__(self):
        return str(self.id) + " | " + self.src_phrase + " | " + self.tar_phrase



class Project(models.Model):
    name = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    src_lang = models.CharField(choices=settings.LANGUAGE, max_length=2)
    tar_lang = models.CharField(choices=settings.LANGUAGE, max_length=2)
    translate_service = MultiSelectField(choices=settings.TRANSLATION_SERVICE)
    translation_memory = models.ManyToManyField(TranslationMemory)
    glossary = models.ManyToManyField(Glossary)

    class Meta:
        unique_together = ('name', 'user',)

    def __str__(self):
        return str(self.id) + " | " + self.name

    def list_glossary(self):
        return ", ".join([p.name for p in self.glossary.all()])

    def list_translation_memory(self):
        return ", ".join([p.name for p in self.translation_memory.all()])
        

class File(models.Model):

    def get_upload_path(instance, filename):
        return os.path.join(settings.DOCUMENT_FOLDER, str(instance.project.id), filename)              

    file = models.FileField(upload_to=get_upload_path, blank=True, null=True, )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    confirm = models.IntegerField()
    
    def __str__(self):
        return str(self.id) + " | " + self.file.name
                
        
class Sentence(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    src_str = models.TextField()
    tar_str = models.TextField(blank=True)
    score = models.FloatField(default=0)
    is_confirmed = models.BooleanField(default=False)
    tag = models.TextField(blank=True)

    def __str__(self):
        return str(self.id) + " | " + self.src_str + " | " + self.tar_str + " | " + str(self.file.id)


class Corpus(models.Model):
    name  = models.TextField()
    language = models.CharField(choices=settings.LANGUAGE, max_length=2)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    description = models.TextField()

    def __str__(self):
        return str(self.id) + " | " + self.name + " | " + self.language
    def get_user_id(self):
        return self.user.id

class CorpusContent(models.Model):
    corpus = models.ForeignKey(Corpus, on_delete=models.CASCADE)
    phrase = models.TextField()

    def __str__(self):
        return str(self.id) + " | " + self.phrase

    class Meta:
        unique_together = ('corpus', 'phrase')   