from django.db import models

PRODUCT_STATE = (
    ('Novo', 'Novo'),
    ('Usado', 'Usado')
)

TAG = (
    ('Oferta do dia', 'Oferta do dia'),
    ('Quente', 'Quente')
)


class Category(models.Model):
    name = models.Charfield(max_length=100)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField()
    
    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"pk": self.pk})

class Product(models.Model):
    name = models.Charfield(max_length=255)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField()
    cover_image = models.ImageField()
    state = models.Charfield(max_length=10, choices=PRODUCT_STATE)
    reviews = models.Charfield(blank=True, null=True)
    tag = models.Charfield(choices=TAG)
    price_old = models.DecimalField(max_digits=10, decimal_places=2)
    price_new = models.DecimalField(max_digits=10., decimal_places=2)
    descount = models.DecimalField(max_digits=10, decimal_places=2)

)
