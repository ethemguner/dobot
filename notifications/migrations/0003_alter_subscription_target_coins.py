# Generated by Django 3.2.9 on 2021-12-18 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coins', '0011_auto_20211218_0023'),
        ('notifications', '0002_auto_20211217_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='target_coins',
            field=models.ManyToManyField(blank=True, to='coins.Coin', verbose_name='Coins targeted'),
        ),
    ]