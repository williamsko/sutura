# Generated by Django 3.1.7 on 2021-05-17 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='identifier',
            field=models.CharField(blank=True, default='1887447147', max_length=50, null=True),
        ),
    ]