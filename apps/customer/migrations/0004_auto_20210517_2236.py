# Generated by Django 3.1.7 on 2021-05-17 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_auto_20210517_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='identifier',
            field=models.CharField(blank=True, default='7963748805', max_length=50, null=True),
        ),
    ]
