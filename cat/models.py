from django.db import models
class TranslationMemory(models.Model):
    src = models.TextField()
    tar = models.TextField()
    
    def __str__(self):
        return self.src + " | " + self.tar
        
# class Glossary(models.Model):
#     src_lang = models.TextField()
#     tar_lang = models.TextField()
#     src_phrase = models.TextField()
#     tar_phrase = models.TextField()
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return self.src + " | " + self.tar
        