# Generated by Django 3.1.7 on 2021-04-03 08:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20210403_0857'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Service',
        ),
        migrations.AlterModelOptions(
            name='productcommandform',
            options={'verbose_name': 'Product form', 'verbose_name_plural': 'Product form'},
        ),
    ]
