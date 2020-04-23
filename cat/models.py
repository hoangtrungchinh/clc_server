from django.db import models
from django.contrib.auth.models import User
import os

class TranslationMemory(models.Model):
    name = models.TextField()
    description = models.TextField()
    src_lang = models.TextField()
    tar_lang = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    
    def __str__(self):
        return str(self.id) + " | " + self.name + " | " + self.src_lang+ " | " + self.tar_lang
        

class TMContent(models.Model):
    src_sentence = models.TextField()
    tar_sentence = models.TextField()
    translation_memory = models.ForeignKey(TranslationMemory, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id) + " | " + self.src_sentence + " | " + self.tar_sentence
        

class GlossaryType(models.Model):
    name = models.TextField()
    description = models.TextField()

    def __str__(self):
        return str(self.id) + " | " + self.name


class Glossary(models.Model):
    name = models.TextField()
    description = models.TextField()
    src_lang = models.TextField()
    tar_lang = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    Type = models.ForeignKey(GlossaryType, on_delete=models.PROTECT)
    
    def __str__(self):
        return str(self.id) + " | " + self.src_lang + " | " + self.tar_lang       


    
class GlossaryContent(models.Model):
    src_phrase = models.TextField()
    tar_phrase = models.TextField()
    glossary = models.ForeignKey(Glossary, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id) + " | " + self.src_phrase + " | " + self.tar_phrase



class Project(models.Model):
    name = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    src_lang = models.TextField()
    tar_lang = models.TextField()
    translate_service = models.TextField()
    translation_memory = models.ManyToManyField(TranslationMemory)
    glossary = models.ManyToManyField(Glossary)
    
    def __str__(self):
        return str(self.id) + " | " + self.name
        

class File(models.Model):

    def get_upload_path(instance, filename):
        return os.path.join('documents', str(instance.project.id), filename)              

    file = models.FileField(upload_to=get_upload_path, blank=False, null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    confirm = models.IntegerField()
    
    def __str__(self):
        return self.file.name
                
        
class Sentence(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    src_str = models.TextField()
    tar_str = models.TextField()
    score = models.FloatField()
    is_confirmed = models.BooleanField()
    tag = models.TextField()

    def __str__(self):
        return str(self.id) + " | " + self.file.name


        