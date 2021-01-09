from django.contrib import admin

from products import models

admin.site.register(models.Product)
admin.site.register(models.Category)
admin.site.register(models.Subcategory)
admin.site.register(models.Review)
admin.site.register(models.ProductImage)
admin.site.register(models.ProductOwner)
admin.site.register(models.Private)
admin.site.register(models.Company)
