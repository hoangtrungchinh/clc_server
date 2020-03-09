from django.db import models
class clc(models.Model):
    src = models.TextField()
    tar = models.TextField()
    
    def __str__(self):
        return self.src + " | " + self.tar
        