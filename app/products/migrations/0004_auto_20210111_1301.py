# Generated by Django 3.1.5 on 2021-01-11 13:01

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20210111_0952'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='images',
        ),
        migrations.RemoveField(
            model_name='productimage',
            name='title',
        ),
        migrations.AddField(
            model_name='productimage',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='products.product'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productimage',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
