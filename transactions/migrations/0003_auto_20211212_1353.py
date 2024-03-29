# Generated by Django 3.2.9 on 2021-12-12 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_transaction_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='coin_amount',
            field=models.DecimalField(blank=True, decimal_places=11, max_digits=19, null=True, verbose_name='Coin Amount Transacted'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='commission_amount',
            field=models.DecimalField(blank=True, decimal_places=11, max_digits=19, null=True, verbose_name='Commission Amount'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='money_amount',
            field=models.DecimalField(blank=True, decimal_places=11, max_digits=19, null=True, verbose_name='Money Amount Transacted'),
        ),
    ]
