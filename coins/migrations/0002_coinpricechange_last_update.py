# Generated by Django 3.2.9 on 2021-11-19 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coins', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coinpricechange',
            name='last_update',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Last Update'),
        ),
    ]
