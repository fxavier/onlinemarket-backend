import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphene_file_upload.scalars import Upload
from django.db.models import Q

from products.models import Category, Subcategory, Product

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category

class SubcategoryType(DjangoObjectType):
    class Meta:
        model = Subcategory

class ProductType(DjangoObjectType):
    class Meta:
        model = Product

class Query(graphene.ObjectType):
    categories = graphene.List(CategoryType)
    subcategories = graphene.List(SubcategoryType)
    subcategories_by_category = graphene.List(SubcategoryType, category_id=graphene.Int())
    products = graphene.List(ProductType, search=graphene.String(), subcategory_id=graphene.Int())
    featured = graphene.List(ProductType)
   

    def resolve_categories(self, info):
        return Category.objects.all()

    def resolve_subcategories(self, info):
        return Subcategory.objects.all()

    def resolve_subcategories_by_category(self, info, category_id):
        return Subcategory.objects.filter(category_id=category_id)


    def resolve_products(self, info, search=None, subcategory_id=None):
        if subcategory_id:
            return Product.objects.filter(subcategory_id=subcategory_id)
        elif search:
            def search(self, query):
                lookups = (
                    Q(name__icontains=query) |
                    Q(description__icontains=query))
                return self.filter(lookups)
        return Product.objects.filter(active=True)
    
    def resolve_featured(self, info):
        return Product.objects.filter(featured=True)

class CreateCategory(graphene.Mutation):
    category = graphene.Field(CategoryType)

    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()

    def mutate(self, info, **fields):
        category = Category(
            name=fields.get('name'),
            description=fields.get('description')
        )
        category.save()
        return CreateCategory(category=category)

class UpdateCategory(graphene.Mutation):
    category = graphene.Field(CategoryType)

    class Arguments:
        category_id = graphene.Int(required=True)
        name = graphene.String()
        description = graphene.String()

    def mutate(self, info, **fields):
        category = Category.objects.get(id=fields.get('category_id'))

        category.name = fields.get('name') 
        category.description = fields.get('description')

        category.save()
        return UpdateCategory(category=category)

class CreateSubcategory(graphene.Mutation):
    subcategory = graphene.Field(SubcategoryType)

    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()
        category_id = graphene.Int(required=True)

    def mutate(self, info, **fields):
        category = Category.objects.get(id=fields.get('category_id'))
        if not category:
            raise GraphQLError('Não existe uma categoria com esse código.')
        subcategory = Subcategory.objects.create(
            name=fields.get('name'),
            description=fields.get('description'),
            category=category
        )
        subcategory.save()
        return CreateSubcategory(subcategory=subcategory)

class UpdateSubcategory(graphene.Mutation):
    subcategory_id = graphene.Int(required=True)

    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()
        category_id = graphene.Int(required=True)

    def mutate(self, info, **fields):
        subcategory = Subcategory.objects.get(id=fields.get('subcategory_id'))

        subcategory.name = fields.get('name')
        subcategory.description = fields.get('description')
        subcategory.category_id = fields.get('category_id')
        subcategory.save()
        return UpdateSubcategory(subcategory=subcategory)


class UploadMutation(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    success = graphene.Boolean()

    def mutate(self, info, file, **kwargs):
        # do something with your file

        return UploadMutation(success=True)

class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    create_subcategory = CreateSubcategory.Field()


