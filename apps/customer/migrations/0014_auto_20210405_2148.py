# Generated by Django 3.1.7 on 2021-04-05 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0013_auto_20210405_2100'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProofContent',
        ),
        migrations.AlterField(
            model_name='customer',
            name='identifier',
            field=models.CharField(blank=True, default='7748471068', max_length=50, null=True),
        ),
    ]