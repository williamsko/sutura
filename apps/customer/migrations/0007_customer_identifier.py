# Generated by Django 3.1.7 on 2021-04-02 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0006_auto_20210402_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='identifier',
            field=models.CharField(default='6478762251', max_length=50, unique=True),
        ),
    ]