import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from coach import models

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class AuthorType(DjangoObjectType):
    class Meta:
        model = models.Profile

class ProgramType(DjangoObjectType):
    class Meta:
        model = models.Program

class TagType(DjangoObjectType):
    class Meta:
        model = models.Tag

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
        body = graphene.String(required=True)
        author = graphene.String(required=True)
        tags = graphene.List(graphene.String)
        slug = graphene.String(required=True)

    def mutate(self, info, title, body, author, tags):
        author = models.Profile.objects.select_related("user").get(user__username=author)
        program = models.Program(title=title, body=body, author=author)
        program.save()
        for tag in tags:
            program.tags.add(models.Tag.objects.get(name=tag))
        return CreateProgram(program=program)
    
class Mutation(graphene.ObjectType):
    create_tag = CreateTag.Field()
    create_program = CreateProgram.Field()

class Query(graphene.ObjectType):
    all_programs = graphene.List(ProgramType)
    author_by_username = graphene.Field(AuthorType, username=graphene.String())
    programs_by_slug = graphene.Field(ProgramType, slug=graphene.String())
    programs_by_author = graphene.List(ProgramType, username=graphene.String())
    programs_by_tag = graphene.List(ProgramType, tag=graphene.String())

    def resolve_all_programs(root, info):
        return (
            models.Program.objects.prefetch_related("tags")
            .select_related("author")
            .all()
        )

    def resolve_author_by_username(root, info, username):
        return models.Profile.objects.select_related("user").get(
            user__username=username
        )

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
            .filter(author__user__username=username)
        )

    def resolve_programs_by_tag(root, info, tag):
        return (
            models.Program.objects.prefetch_related("tags")
            .select_related("author")
            .filter(tags__name__iexact=tag)
        )

    
schema = graphene.Schema(query=Query, mutation=Mutation)