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
    order_in_day = models.IntegerField(null=True, blank=True)
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='workouts', null=True, blank=True)

class Block(models.Model):
    name = models.CharField(max_length=255)
    order_in_workout = models.IntegerField()
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='blocks')

    def __str__(self):
        return self.name

class Exercise(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    order_in_block = models.IntegerField()
    #the sets and reps should likely be their own model with a foreign key to exercise
    #because they will may be different for each user & should encompass percent of 1RM  
    block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name='exercises')
    
    def __str__(self):
        return self.name
    
class Set(models.Model):
    reps = models.IntegerField()
    weight = models.IntegerField()
    number = models.IntegerField()
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='sets')
    
    
    def __str__(self):
        return f'{self.reps} @ {self.weight}'
    
class LoggedWorkout(models.Model):
    athlete = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logged_workouts')
    assigned_date = models.DateTimeField()
    date = models.DateTimeField(auto_now_add=True)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='logged_workouts')
    notes = models.TextField()
    
    
    def __str__(self):
        return f'{self.athlete} {self.date} {self.workout}'
    

class LoggedSet(models.Model):
    set = models.ForeignKey(Set, on_delete=models.CASCADE, related_name='logged_sets')
    reps_completed = models.IntegerField()
    weight_completed = models.IntegerField()
    logged_workout = models.ForeignKey(LoggedWorkout, on_delete=models.CASCADE, related_name='logged_sets')
    
    def __str__(self):
        return f'{self.set} {self.reps_completed} @ {self.weight_completed}'
    
class WorkoutGroup(models.Model):
    coach = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coached_workout_groups')
    name = models.CharField(max_length=255)
    athletes = models.ManyToManyField(User, related_name='athlete_workout_groups', blank=True)

    def __str__(self):
        return self.name
    
