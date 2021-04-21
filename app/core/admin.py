from django.contrib import admin

from products.models import Product, Category, Subcategory, ProductOwner, ProductImage, \
     CategoryImage, Private, Company

from users.models import User

classes = [Product, Category, Subcategory, ProductOwner, ProductImage, Private, Company, User, CategoryImage]

for model in classes:
    admin.site.register(model)