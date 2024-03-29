# Generated by Django 3.2.9 on 2021-12-17 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coins', '0010_alter_coin_symbol'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coinpricechange',
            name='change',
            field=models.DecimalField(decimal_places=5, max_digits=19, verbose_name='Change'),
        ),
        migrations.AlterField(
            model_name='coinpricechange',
            name='change_ratio',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=19, null=True, verbose_name='Change'),
        ),
        migrations.AlterField(
            model_name='coinpricechange',
            name='price',
            field=models.DecimalField(decimal_places=5, max_digits=19, verbose_name='Price'),
        ),
    ]
