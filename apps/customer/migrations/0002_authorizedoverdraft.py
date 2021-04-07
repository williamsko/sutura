# Generated by Django 3.1.7 on 2021-02-19 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorizedOverDraft',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('overdraft_amount', models.DecimalField(decimal_places=2, default=0, help_text='Overdraft amount', max_digits=9)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='customer.customer')),
            ],
            options={
                'verbose_name': 'Authorized overdraft',
                'verbose_name_plural': 'Authorized overdraft',
            },
        ),
    ]