# Generated by Django 3.2.9 on 2021-12-05 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coins', '0006_alter_coinpricechange_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='coinpricechange',
            name='change_ratio',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=19, null=True, verbose_name='Change'),
        ),
    ]