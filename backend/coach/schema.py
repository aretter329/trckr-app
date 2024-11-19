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

class LoggedWorkoutType(DjangoObjectType):
    class Meta:
        model = models.LoggedWorkout

class LoggedSetType(DjangoObjectType):
    class Meta:
        model = models.LoggedSet


class BlockType(DjangoObjectType):
    class Meta:
        model = models.Block

class SetInputType(graphene.InputObjectType):
    reps = graphene.Int()
    weight = graphene.Int()
    number = graphene.Int()

class ExerciseInputType(graphene.InputObjectType):
    name = graphene.String()
    description = graphene.String()
    order_in_block = graphene.Int()
    sets = graphene.List(SetInputType)

class BlockInputType(graphene.InputObjectType):
    name = graphene.String()
    order_in_workout = graphene.Int()
    exercises = graphene.List(ExerciseInputType)

class WorkoutInputType(graphene.InputObjectType):
    type = graphene.String()
    order_in_day = graphene.Int()
    blocks = graphene.List(BlockInputType)

class DayInputType(graphene.InputObjectType):
    name = graphene.String()
    order_in_program = graphene.Int()
    workouts = graphene.List(WorkoutInputType)

class LoggedSetInput(graphene.InputObjectType):
    set_id = graphene.ID()
    reps_completed = graphene.Int()
    weight_completed = graphene.Int()

class LoggedWorkoutInput(graphene.InputObjectType):
    athlete_username = graphene.String()
    notes = graphene.String()
    workout_id = graphene.ID()
    date = graphene.Date()
    sets = graphene.List(LoggedSetInput)

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
        assigned_athletes = graphene.List(graphene.String)
        days = graphene.List(DayInputType)

    def mutate(self, info, title, notes, author, tags, slug, assigned_athletes, days):
        author = models.User.objects.get(username=author)
        program = models.Program(title=title, notes=notes, author=author, slug=slug)
        program.save()
        for tag in tags:
            program.tags.add(models.Tag.objects.get(name=tag))
        athletes  = models.User.objects.filter(username__in=assigned_athletes)
        program.assigned_athletes.set(athletes)
        
        for day in days:
            day_obj = models.Day(name=day.name, order_in_program=day.order_in_program, program=program)
            day_obj.save()
            for workout in day.workouts:
                workout_obj = models.Workout(type=workout.type, order_in_day=workout.order_in_day, day=day_obj)
                workout_obj.save()
                for block in workout.blocks:
                    block_obj = models.Block(name=block.name, order_in_workout=block.order_in_workout, workout=workout_obj)
                    block_obj.save()
                    for exercise in block.exercises:
                        exercise_obj = models.Exercise(name=exercise.name, description=exercise.description, order_in_block=exercise.order_in_block, block=block_obj)
                        exercise_obj.save()
                        for set in exercise.sets:
                            set_obj = models.Set(reps=set.reps, weight=set.weight, number=set.number, exercise=exercise_obj)
                            set_obj.save()

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
        order_in_block = graphene.Int(required=False)
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
        is_athlete = graphene.Boolean(required=True)
        is_coach = graphene.Boolean(required=True)
        coach = graphene.String(required=False)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=False)  

    def mutate(self, info, username, email, password, is_coach, is_athlete, first_name, last_name=None, coach=None):  
        user = models.User(
            username=username, 
            email=email,
            is_coach=is_coach,
            is_athlete=is_athlete,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        if coach:
            coach_user = models.User.objects.get(username=coach)
            user.coach = coach_user
        user.save()
        return CreateUser(user=user)
    
class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)
    
class AddAthlete(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        athlete_username = graphene.String(required=True)
        coach_username = graphene.String(required=True)

    def mutate(self, info, athlete_username, coach_username):
        athlete = models.User.objects.get(username=athlete_username)
        coach = models.User.objects.get(username=coach_username)
        athlete.coach = coach
        athlete.save()
        return AddAthlete(user=athlete)
    
class AssignProgram(graphene.Mutation):
    program = graphene.Field(ProgramType)

    class Arguments:
        program_id = graphene.ID(required=True)
        athlete_username = graphene.String(required=True)

    def mutate(self, info, program_id, athlete_username):
        program = models.Program.objects.get(id=program_id)
        athlete = models.User.objects.get(username=athlete_username)
        program.assigned_athletes.add(athlete)
        program.save()
        return AssignProgram(program=program)
    
class LogWorkout(graphene.Mutation):
    class Arguments: 
        athlete_username = graphene.String(required=True)
        workout_id = graphene.ID(required=True)
        sets = graphene.List(LoggedSetInput)
        notes = graphene.String(required=False)
        assigned_date = graphene.Date(required=False)
    
    logged_workout = graphene.Field(LoggedWorkoutType)

    def mutate(self, info, athlete_username, notes, workout_id, sets, assigned_date=None):  
        athlete = models.User.objects.get(username=athlete_username)
        workout = models.Workout.objects.get(id=workout_id)
        logged_workout = models.LoggedWorkout(athlete=athlete, workout=workout, notes=notes, assigned_date=assigned_date)
        logged_workout.save()
        for set in sets:
            logged_set = models.LoggedSet(set=models.Set.objects.get(id=set.set_id), reps_completed=set.reps_completed, weight_completed=set.weight_completed, logged_workout=logged_workout)
            logged_set.save()
        return LogWorkout(logged_workout=logged_workout)

    
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
    add_athlete = AddAthlete.Field()
    assign_program = AssignProgram.Field()
    log_workout = LogWorkout.Field()

class Query(graphene.ObjectType):
    all_programs = graphene.List(ProgramType)
    author_by_username = graphene.Field(AuthorType, username=graphene.String())
    programs_by_slug = graphene.Field(ProgramType, slug=graphene.String())
    programs_by_author = graphene.List(ProgramType, username=graphene.String())
    programs_by_tag = graphene.List(ProgramType, tag=graphene.String())
    days_by_program = graphene.List(DayType, program_id=graphene.ID())
    workouts_by_day = graphene.List(WorkoutType, day_id=graphene.ID())
    blocks_by_workout = graphene.List(BlockType, workout_id=graphene.ID())
    exercises_by_block = graphene.List(ExerciseType, block_id=graphene.ID())
    sets_by_exercise = graphene.List(SetType, exercise_id=graphene.ID())
    program_days = graphene.List(DayType, program_id=graphene.ID())
    all_athletes_by_coach = graphene.List(UserType, coach_username=graphene.String())
    programs_by_athlete = graphene.List(ProgramType, athlete_username=graphene.String())
    logged_workouts_by_athlete = graphene.List(LoggedWorkoutType, athlete_username=graphene.String())
    logged_sets_by_workout = graphene.List(LoggedSetType, workout_id=graphene.ID())
    get_program_workouts = graphene.List(WorkoutType, program_id=graphene.ID())
    get_logged_workouts_by_athlete = graphene.List(LoggedWorkoutType, athlete_username=graphene.String())
    assigned_workouts_by_athlete_and_date = graphene.List(LoggedWorkoutType, athlete_username=graphene.String(), assigned_date=graphene.Date())
    workout_by_id = graphene.Field(WorkoutType, workout_id=graphene.ID())

    def resolve_logged_workouts_by_athlete(root, info, athlete_username):
        athlete = models.User.objects.get(username=athlete_username)
        return models.LoggedWorkout.objects.filter(athlete=athlete)
    
    def resolve_logged_sets_by_workout(root, info, workout_id):
        return models.LoggedSet.objects.filter(logged_workout__id=workout_id)

    def resolve_program_days(root, info, program_id):
        program = models.Program.objects.get(id=program_id)
        return program.days.prefetch_related("workouts__blocks__exercises__sets")

    def resolve_sets_by_exercise(root, info, exercise_id):
        return models.Set.objects.filter(exercise_id=exercise_id)
    
    def resolve_blocks_by_workout(root, info, workout_id): 
        return models.Block.objects.filter(workout_id=workout_id)

    def resolve_exercises_by_block(root, info, block_id):
        return models.Exercise.objects.filter(block_id=block_id)
                                              
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
    
    def resolve_all_athletes_by_coach(root, info, coach_username):
        coach = models.User.objects.get(username=coach_username)
        return models.User.objects.filter(coach=coach)
    
    def resolve_programs_by_athlete(root, info, athlete_username):
        athlete = models.User.objects.get(username=athlete_username)
        return models.Program.objects.filter(assigned_athletes=athlete)
    
    def resolve_get_program_workouts(root, info, program_id):
        return models.Workout.objects.filter(day__program_id=program_id)
    
    def resolve_get_logged_workouts_by_athlete(root, info, athlete_username):
        athlete = models.User.objects.get(username=athlete_username)
        return models.LoggedWorkout.objects.filter(athlete=athlete)
    
    def resolve_assigned_workouts_by_athlete_and_date(root, info, athlete_username, assigned_date):
        athlete = models.User.objects.get(username=athlete_username)
        return models.LoggedWorkout.objects.filter(athlete=athlete, assigned_date=assigned_date)
    
    def resolve_workout_by_id(root, info, workout_id):
        return models.Workout.objects.get(id=workout_id)
    
schema = graphene.Schema(query=Query, mutation=Mutation)