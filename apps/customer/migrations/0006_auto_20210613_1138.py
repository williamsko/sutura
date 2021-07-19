# Generated by Django 3.1.7 on 2021-06-13 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_auto_20210613_0936'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankInstitution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Bank',
                'verbose_name_plural': 'Banks',
            },
        ),
        migrations.AlterModelOptions(
            name='deliveryaddress',
            options={'verbose_name': 'Delivery address', 'verbose_name_plural': 'Delivery addresses'},
        ),
        migrations.AlterField(
            model_name='customer',
            name='identifier',
            field=models.CharField(blank=True, default='0674308526', max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='BankInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iban', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='customer.bankinstitution')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='customer.customer')),
            ],
            options={
                'verbose_name': 'Bank account information',
                'verbose_name_plural': 'Bank account informations',
            },
        ),
    ]