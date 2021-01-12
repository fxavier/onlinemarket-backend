import graphene
import products.schema
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations


class AuthMutation(graphene.ObjectType):
   register = mutations.Register.Field()
   verify_account = mutations.VerifyAccount.Field()
class Query(UserQuery, MeQuery, products.schema.Query, graphene.ObjectType):
    pass
class Mutation(AuthMutation, products.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)