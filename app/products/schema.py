import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphene_file_upload.scalars import Upload
from django.db.models import Q

from products.models import Category, Subcategory, Product, ProductOwner, Private, Company

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category

class SubcategoryType(DjangoObjectType):
    class Meta:
        model = Subcategory

class ProductType(DjangoObjectType):
    class Meta:
        model = Product

class ProductOwnerType(DjangoObjectType):
    class Meta:
        model = ProductOwner

class PrivateType(DjangoObjectType):
    class Meta:
        model = Private
class CompanyType(DjangoObjectType):
    class Meta:
        model = Company
class Query(graphene.ObjectType):
    categories = graphene.List(CategoryType)
    subcategories = graphene.List(SubcategoryType)
    subcategories_by_category = graphene.List(SubcategoryType, category_id=graphene.Int())
    productOwners = graphene.List(ProductOwnerType)
    privateOwners = graphene.List(PrivateType)
    companyOwners = graphene.List(CompanyType)
    products = graphene.List(ProductType, search=graphene.String(), subcategory_id=graphene.Int())
    featured = graphene.List(ProductType)
   

    def resolve_categories(self, info):
        return Category.objects.all()

    def resolve_subcategories(self, info):
        return Subcategory.objects.all()

    def resolve_subcategories_by_category(self, info, category_id):
        return Subcategory.objects.filter(category_id=category_id)

    def resolve_privateOwners(self,info):
        return Private.objects.all()
    
    def resolve_companyOwners(self, info):
        return Company.objects.all()

    def resolve_productOwners(self, info):
        return ProductOwner.objects.all()

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
class CreatePrivate(graphene.Mutation):
    private = graphene.Field(PrivateType)
    class Arguments:
        name              = graphene.String(required=True)
        email             = graphene.String(required=True)
        phones            = graphene.String()
        address           = graphene.String()
        owner_type        = graphene.String()
        identity_document = graphene.String()

    def mutate(self, info, **fields):
        private = Private(
            name=fields.get('name'),
            email=fields.get('email'),
            phones=fields.get('phones'),
            address=fields.get('address'),
            owner_type=fields.get('owner_type'),
            identity_document = fields.get('identity_document')
            )
        private.save()
        return CreatePrivate(private=private)

class CreateCompany(graphene.Mutation):
    company = graphene.Field(CompanyType)
    class Arguments:
        name       = graphene.String(required=True)
        email      = graphene.String(required=True)
        phones     = graphene.String()
        address    = graphene.String()
        owner_type = graphene.String()
        nuit       = graphene.String()

    def mutate(self, info, **fields):
        company = Company(
            name=fields.get('name'),
            email=fields.get('email'),
            phones=fields.get('phones'),
            address=fields.get('address'),
            owner_type=fields.get('owner_type'),
            nuit=fields.get('nuit')
            )
        company.save()
        return CreateCompany(company=company)

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
    create_private = CreatePrivate.Field()
    create_company = CreateCompany.Field()


