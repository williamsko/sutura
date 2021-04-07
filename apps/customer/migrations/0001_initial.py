# Generated by Django 3.1.7 on 2021-02-19 13:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('phone_number', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
            },
        ),
        migrations.CreateModel(
            name='ProofContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
                ('status', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Document',
                'verbose_name_plural': 'Documents',
            },
        ),
        migrations.CreateModel(
            name='ProofType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('short_name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'Proof type',
                'verbose_name_plural': 'Poofs type',
            },
        ),
        migrations.CreateModel(
            name='Proofs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('content', models.ManyToManyField(to='customer.ProofContent')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='customer.customer')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='customer.prooftype')),
            ],
            options={
                'verbose_name': 'Proof',
                'verbose_name_plural': 'Proofs',
            },
        ),
    ]