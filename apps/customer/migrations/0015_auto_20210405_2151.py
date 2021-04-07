# Generated by Django 3.1.7 on 2021-04-05 21:51

import apps.customer.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0014_auto_20210405_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='identifier',
            field=models.CharField(blank=True, default='7625379206', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='proofs',
            name='content',
            field=models.ImageField(blank=True, null=True, upload_to=apps.customer.models.proof_directory_path, validators=[apps.customer.models.validate_file_extension]),
        ),
    ]
