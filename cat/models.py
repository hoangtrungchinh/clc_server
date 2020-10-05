from django.db import models
from django.contrib.auth.models import User
import os
import sys
from django.conf import settings
from multiselectfield import MultiSelectField

from django.db.models.signals import post_save
from django.dispatch import receiver

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
  translate_service = MultiSelectField(choices=settings.TRANSLATION_SERVICE, max_length=200)
  glossary = models.ManyToManyField(Glossary)
  searchable_translation_memory = models.ManyToManyField(TranslationMemory)
  writable_translation_memory = models.ForeignKey(TranslationMemory, on_delete=models.PROTECT, related_name='%(class)s_requests_insert')

  class Meta:
    unique_together = ('name', 'user',)

  def __str__(self):
    return str(self.id) + " | " + self.name

  def list_glossary(self):
    return ", ".join([p.name for p in self.glossary.all()])

  def list_translation_memory(self):
    return ", ".join([p.name for p in self.searchable_translation_memory.all()])


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
  tm_content = models.ForeignKey(TMContent , blank=True, null=True, on_delete=models.SET_NULL)

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


class Config(models.Model):
  user = models.ForeignKey(User, on_delete=models.PROTECT)
  min_similarity_for_gloss  = models.FloatField(default=0.8)
  min_similarity_for_tm  = models.FloatField(default=0.8)
  similarity_type = models.CharField(max_length=20, choices=settings.SIMILARITY_TYPE, default=settings.SIMILARITY_TYPE[0][0])

  def __str__(self):
    return str(self.id) + " | " + str(self.user.id) + " | " + str(self.min_similarity_for_gloss) + " | " + str(self.min_similarity_for_tm) + " | " + str(self.similarity_type)

  def get_user_id(self):
    return self.user.id
  class Meta:
    unique_together = ('user', 'min_similarity_for_gloss', 'min_similarity_for_tm', 'similarity_type')


@receiver(post_save, sender=User)
def create_config(sender, instance, created, **kwargs):
  if created:
    Config.objects.create(user=instance, min_similarity_for_gloss=0.8, min_similarity_for_tm=0.8, similarity_type = settings.SIMILARITY_TYPE[0][0])