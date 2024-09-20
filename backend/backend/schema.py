from coach.schema import schema as coach_schema
#from user.schema import schema as user_schema
import graphene

class Query(coach_schema.Query):
  pass

class Mutation(coach_schema.Mutation):
  pass

schema = graphene.Schema(query=Query, mutation=Mutation)
