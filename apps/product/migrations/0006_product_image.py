# Generated by Django 3.1.7 on 2021-04-03 16:11

import apps.product.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_delete_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=apps.product.models.product_image_directory_path),
        ),
    ]
