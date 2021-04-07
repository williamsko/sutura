# Generated by Django 3.1.7 on 2021-04-02 16:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_category_image_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='product',
        ),
        migrations.RemoveField(
            model_name='product',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='country',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='phone_number',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Image',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
