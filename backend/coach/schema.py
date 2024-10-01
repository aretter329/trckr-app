import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from coach import models
import graphql_jwt

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class AuthorType(DjangoObjectType):
    class Meta:
        model = models.User

class ProgramType(DjangoObjectType):
    class Meta:
        model = models.Program

class TagType(DjangoObjectType):
    class Meta:
        model = models.Tag

class ExerciseType(DjangoObjectType):
    class Meta:
        model = models.Exercise

class DayType(DjangoObjectType):
    class Meta:
        model = models.Day

class WorkoutType(DjangoObjectType):
    class Meta:
        model = models.Workout

class SetType(DjangoObjectType):
    class Meta:
        model = models.Set

class CreateTag(graphene.Mutation):
    tag = graphene.Field(TagType)

    class Arguments:
        name = graphene.String(required=True)

    def mutate(self, info, name):
        tag = models.Tag(name=name)
        tag.save()
        return CreateTag(tag=tag)
    
class CreateProgram(graphene.Mutation):
    program = graphene.Field(ProgramType)

    class Arguments:
        title = graphene.String(required=True)
        notes = graphene.String(required=True)
        author = graphene.String(required=True)
        tags = graphene.List(graphene.String)
        slug = graphene.String(required=True)

    def mutate(self, info, title, notes, author, tags, slug):
        author = models.User.objects.get(username=author)
        program = models.Program(title=title, notes=notes, author=author, slug=slug)
        program.save()
        for tag in tags:
            program.tags.add(models.Tag.objects.get(name=tag))
        return CreateProgram(program=program)
    
class CreateDay(graphene.Mutation):
    day = graphene.Field(DayType)

    class Arguments:
        name = graphene.String(required=True)
        order_in_program = graphene.Int(required=True)
        program_id = graphene.ID(required=True)

    def mutate(self, info, name, order_in_program, program_id):
        program = models.Program.objects.get(id=program_id)
        day = models.Day(
            name=name,
            order_in_program=order_in_program,
            program=program
        )
        day.save()
        return CreateDay(day=day)
    
class CreateWorkout(graphene.Mutation):
    workout = graphene.Field(WorkoutType)

    class Arguments:
        type = graphene.String(required=True)
        order_in_day = graphene.Int(required=True)
        day_id = graphene.ID(required=True)

    def mutate(self, info, type, order_in_day, day_id):
        day = models.Day.objects.get(id=day_id)
        workout = models.Workout(
            type=type,
            order_in_day=order_in_day,
            day=day
        )
        workout.save()
        return CreateWorkout(workout=workout)

class CreateExercise(graphene.Mutation):
    exercise = graphene.Field(ExerciseType)

    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        block = graphene.Int(required=True)
        order_in_block = graphene.Int(required=True)
        workout_id = graphene.ID(required=True)  # Modified argument

    def mutate(self, info, name, description, block, order_in_block, workout_id):  # Modified argument
        workout = models.Workout.objects.get(id=workout_id)  # Modified code to get workout by id
        exercise = models.Exercise(
            name=name,
            description=description,
            block=block,
            order_in_block=order_in_block,
            workout=workout
        )
        exercise.save()
        return CreateExercise(exercise=exercise)
    
class CreateSet(graphene.Mutation):
    set = graphene.Field(SetType)

    class Arguments:
        reps = graphene.Int(required=True)
        weight = graphene.Int(required=True)
        exercise_id = graphene.ID(required=True)
        number = graphene.Int(required=True)

    def mutate(self, info, reps, weight, number, exercise_id):
        exercise = models.Exercise.objects.get(id=exercise_id)
        set = models.Set(
            reps=reps,
            number = number,
            weight=weight,
            exercise=exercise
        )
        set.save()
        return CreateSet(set=set)

class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, email, password):
        user = models.User(
            username=username, 
            email=email
        )
        user.set_password(password)
        user.save()
        return CreateUser(user=user)
class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)
    
class Mutation(graphene.ObjectType):
    create_tag = CreateTag.Field()
    create_program = CreateProgram.Field()
    create_user = CreateUser.Field()
    token_auth = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    create_exercise = CreateExercise.Field()
    create_day = CreateDay.Field()
    create_workout = CreateWorkout.Field()
    create_set = CreateSet.Field()

class Query(graphene.ObjectType):
    all_programs = graphene.List(ProgramType)
    author_by_username = graphene.Field(AuthorType, username=graphene.String())
    programs_by_slug = graphene.Field(ProgramType, slug=graphene.String())
    programs_by_author = graphene.List(ProgramType, username=graphene.String())
    programs_by_tag = graphene.List(ProgramType, tag=graphene.String())
    days_by_program = graphene.List(DayType, program_id=graphene.ID())
    workouts_by_day = graphene.List(WorkoutType, day_id=graphene.ID())
    exercises_by_workout = graphene.List(ExerciseType, workout_id=graphene.ID())
    sets_by_exercise = graphene.List(SetType, exercise_id=graphene.ID())

    def resolve_sets_by_exercise(root, info, exercise_id):
        return models.Set.objects.filter(exercise_id=exercise_id)

    def resolve_exercises_by_workout(root, info, workout_id):
        return models.Exercise.objects.filter(workout_id=workout_id)
                                              
    def resolve_workouts_by_day(root, info, day_id):
        return models.Workout.objects.filter(day_id=day_id)

    def resolve_days_by_program(root, info, program_id):
        return models.Day.objects.filter(program_id=program_id)

    def resolve_all_programs(root, info):
        return (
            models.Program.objects.prefetch_related("tags")
            .select_related("author")
            .all()
        )

    def resolve_author_by_username(root, info, username):
        return models.User.objects.get(username=username)

    def resolve_programs_by_slug(root, info, slug):
        return (
            models.Program.objects.prefetch_related("tags")
            .select_related("author")
            .get(slug=slug)
        )

    def resolve_programs_by_author(root, info, username):
        return (
            models.Program.objects.prefetch_related("tags")
            .select_related("author")
            .filter(author__username=username)
        )

    def resolve_programs_by_tag(root, info, tag):
        return (
            models.Program.objects.prefetch_related("tags")
            .select_related("author")
            .filter(tags__name__iexact=tag)
        )

    
schema = graphene.Schema(query=Query, mutation=Mutation)