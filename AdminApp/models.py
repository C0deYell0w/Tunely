from django.db import models

# Create your models here.
class Genre(models.Model):
    Genre_Name = models.CharField(max_length=50)
    Genre_Icons = models.ImageField(upload_to='Genre_Icons/', blank=True, null=True)

class Language(models.Model):
    Lang = models.CharField(max_length=50)
    Lang_Char = models.CharField(max_length=50,blank=True, null=True)

class MusicMood(models.Model):
    Mood = models.CharField(max_length=50)

class Admindata(models.Model):
    mail = models.EmailField(unique=True)
    Password = models.CharField(max_length = 150)
    