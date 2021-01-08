# Generated by Django 3.1.5 on 2021-01-07 15:05

import core.utils
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to=core.utils.category_image_file_path)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('description', models.TextField()),
                ('cover_image', models.ImageField(upload_to=core.utils.product_image_file_path)),
                ('state', models.CharField(choices=[('Novo', 'Novo'), ('Usado', 'Usado')], max_length=10)),
                ('tag', models.CharField(choices=[('Oferta do dia', 'Oferta do dia'), ('Quente', 'Quente'), ('Mais vendido', 'Mais Vendido')], max_length=100)),
                ('price_old', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price_new', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.IntegerField(default=1)),
                ('active', models.BooleanField(default=True)),
                ('featured', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=core.utils.product_image_file_path)),
            ],
        ),
        migrations.CreateModel(
            name='ProductOwner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phones', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), size=None)),
                ('endereco', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('productowner_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='products.productowner')),
                ('nuit', models.CharField(max_length=150)),
                ('logo', models.ImageField(null=True, upload_to=core.utils.company_image_file_path)),
            ],
            bases=('products.productowner',),
        ),
        migrations.CreateModel(
            name='Private',
            fields=[
                ('productowner_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='products.productowner')),
                ('identity_document', models.CharField(blank=True, max_length=50, null=True)),
            ],
            bases=('products.productowner',),
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.category')),
            ],
            options={
                'verbose_name': 'Subcategory',
                'verbose_name_plural': 'Subcategories',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='images',
            field=models.ManyToManyField(to='products.ProductImage'),
        ),
        migrations.AddField(
            model_name='product',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='products.productowner'),
        ),
        migrations.AddField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.subcategory'),
        ),
    ]