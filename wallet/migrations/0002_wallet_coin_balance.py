# Generated by Django 3.2.9 on 2021-12-04 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='coin_balance',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True, verbose_name='Total Balance'),
        ),
    ]
