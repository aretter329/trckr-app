from django.db import models
from django.conf import settings 
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_athlete = models.BooleanField(default=True)
    is_coach = models.BooleanField(default=False)
    coach = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='athletes')
    
    def __str__(self):
        return self.username

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
class Program(models.Model):
  title = models.CharField(max_length=255, unique=True)
  slug = models.SlugField(max_length=255, unique=True)
  notes = models.TextField()
  date_created = models.DateTimeField(auto_now_add=True)
  date_modified = models.DateTimeField(auto_now=True)
  published = models.BooleanField(default=False)
  author = models.ForeignKey(User, on_delete=models.PROTECT)
  tags = models.ManyToManyField(Tag, blank=True)
  assigned_athletes = models.ManyToManyField(User, related_name='assigned_programs', blank=True)

  class Meta:
      ordering = ["-date_created"]

class Day(models.Model):
    name = models.CharField(max_length=255)
    order_in_program = models.IntegerField()
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='days')

    def __str__(self):
        return self.name
    
class Workout(models.Model):
    type = models.CharField(max_length=255)
    order_in_day = models.IntegerField()
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='workouts')

    

class Exercise(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    block = models.IntegerField()
    order_in_block = models.IntegerField()
    #the sets and reps should likely be their own model with a foreign key to exercise
    #because they will may be different for each user & should encompass percent of 1RM  
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='exercises')

    def __str__(self):
        return self.name
    
class Set(models.Model):
    reps = models.IntegerField()
    weight = models.IntegerField()
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='sets')
    number = models.IntegerField()
    
    def __str__(self):
        return f'{self.reps} @ {self.weight}'