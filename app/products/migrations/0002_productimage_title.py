# Generated by Django 3.1.5 on 2021-01-11 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='title',
            field=models.CharField(default='Title', max_length=100),
            preserve_default=False,
        ),
    ]
