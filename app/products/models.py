from django.db import models
from django.db.models import Q
from django.contrib.postgres.fields import ArrayField
from decimal import Decimal

from core.utils import product_image_file_path, category_image_file_path, unique_slug_generator, company_image_file_path

from django.db.models.signals import pre_save, post_save


PRODUCT_STATE = (
    ('Novo', 'Novo'),
    ('Usado', 'Usado')
)

TAG = (
    ('Oferta do dia', 'Oferta do dia'),
    ('Quente', 'Quente'),
    ('Mais vendido', 'Mais Vendido')
)

OWNER_TYPE = (
    ('Particular', 'Particular'),
    ('Empresa', 'Empresa')
)

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField()
   # image = models.ImageField(blank=True, null=True, upload_to=category_image_file_path)
    
    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"pk": self.pk})
    
class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Subcategory"
        verbose_name_plural = "Subcategories"
    
    def __str__(self):
        return self.name

    
    # def __str__(self):
    #     return self.id
    
# class ProductQuerySet(models.query.QuerySet):
#     def active(self):
#         return self.filter(active=True) 
    
#     def featured(self):
#         return self.filter(featured=True)
    
#     def search(self, query):
#         lookups = (Q(name__icontains=query) |
#                    Q(description__icontains=query) |
#                    Q(price_new__icontains=query)
#                    )
#         return self.filter(lookups)

# class ProductManager(models.Manager):
#     def get_queryset(self):
#         return ProductQuerySet(self.model, using=self._db)
    
#     def all(self):
#         return get_queryset().active()
        
#     def featured(self):
#         return get_queryset().featured()
    
#     def get_by_id(self, id):
#         qs = self.get_queryset().filter(id=id)
#         if qs.count == 1:
#             return qs.first()
#         return None
    
#     def search(self, query):
#         return self.get_queryset().active().search(query)

class ProductOwner(models.Model):
    name = models.CharField(max_length = 255)
    email = models.EmailField(max_length=254)
    phones = ArrayField(models.CharField(max_length=50))
    address = models.CharField(max_length=255)
    owner_type = models.CharField(max_length=20, choices=OWNER_TYPE)


    def __str__(self):
        return self.name

class Private(ProductOwner):
    identity_document = models.CharField(max_length=50, null=True, blank=True)

class Company(ProductOwner):
    vat_number = models.CharField(max_length = 150)
    logo = models.ImageField(upload_to=company_image_file_path , null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Companies'
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField()
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    state = models.CharField(max_length=10, choices=PRODUCT_STATE)
    tag = models.CharField(max_length=100, choices=TAG)
    price_old = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    price_new = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=Decimal("0.00"))
    quantity = models.IntegerField(default=1)
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    product_owner = models.ForeignKey(ProductOwner, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class CategoryImage(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    url = models.CharField(max_length = 255)
    
    class Meta:
        verbose_name = 'Category Image'
        verbose_name_plural = 'Category Images'
        
    def __str__(self):
        return self.category.name
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    url = models.CharField(max_length = 255)
    
    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'
    
    def __str__(self):
        return self.product.name
        
    
   # objects = ProductManager()
    
# class Review(models.Model):
#     comment = models.TextField(blank=True, null=True)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return self.product.name       

def category_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        
pre_save.connect(category_pre_save_receiver, sender=Category)

def subcategory_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        
pre_save.connect(subcategory_pre_save_receiver, sender=Subcategory)
   
def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        
pre_save.connect(product_pre_save_receiver, sender=Product)

def price_new_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.price_new:
        instance.price_new = instance.price_old * (1 - instance.discount / 100)

pre_save.connect(price_new_pre_save_receiver, sender=Product)