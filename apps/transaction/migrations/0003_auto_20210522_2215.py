# Generated by Django 3.1.7 on 2021-05-22 22:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_auto_20210517_2237'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='command',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='transaction.command'),
        ),
        migrations.AlterField(
            model_name='command',
            name='identifier',
            field=models.CharField(blank=True, default='5268057651', max_length=50, null=True),
        ),
    ]
