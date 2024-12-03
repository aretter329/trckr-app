from django.contrib import admin
from coach.models import Program, Tag, User, Exercise, Workout, Day, Set, Block, LoggedWorkout, LoggedSet, WorkoutGroup, ExerciseName


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('username', 'first_name', 'last_name', 'email', 'date_joined')
    

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    model = Program



    list_display = (
        "id",
        "title",
        "slug",
        "date_created",
        "published",
    )
    list_filter = (
        "published",
        "date_created",
    )
    list_editable = (
        "title",
        "slug",
        "published",
    )
    search_fields = (
        "title",
        "slug",
        "body",
    )
    prepopulated_fields = {
        "slug": (
            "title",
        )
    }
    date_hierarchy = "date_created"
    save_on_top = True

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    model = Exercise
    
@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    model = Workout

@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    model = Day
    
@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    model = Set
    list_display = ('id', 'reps', 'weight', 'number')

@admin.register(Block)
class SetAdmin(admin.ModelAdmin):
    model = Block

@admin.register(LoggedWorkout)
class LoggedWorkoutAdmin(admin.ModelAdmin):
    model = LoggedWorkout
    list_display = ('id', 'date', 'workout', 'athlete')

@admin.register(LoggedSet)
class LoggedSetAdmin(admin.ModelAdmin):
    model = LoggedSet
    list_display = ('id', 'reps_completed', 'weight_completed')

@admin.register(WorkoutGroup)
class WorkoutGroupAdmin(admin.ModelAdmin):
    model = WorkoutGroup
    list_display = ('id', 'name', 'coach')

@admin.register(ExerciseName)
class ExerciseNameAdmin(admin.ModelAdmin):
    model = ExerciseName
    list_display = ('id', 'name', 'author')