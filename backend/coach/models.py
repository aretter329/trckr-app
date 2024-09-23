from django.db import models
from django.conf import settings 
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    
    def __str__(self):
        return self.username  

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
class Program(models.Model):
  title = models.CharField(max_length=255, unique=True)
  slug = models.SlugField(max_length=255, unique=True)
  body = models.TextField()
  date_created = models.DateTimeField(auto_now_add=True)
  date_modified = models.DateTimeField(auto_now=True)
  published = models.BooleanField(default=False)
  author = models.ForeignKey(User, on_delete=models.PROTECT)
  tags = models.ManyToManyField(Tag, blank=True)

  class Meta:
      ordering = ["-date_created"]
