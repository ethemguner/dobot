# Generated by Django 3.2.9 on 2021-12-19 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('decision_maker', '0006_decision_wallet'),
    ]

    operations = [
        migrations.AddField(
            model_name='decisionsetting',
            name='allocated_money_amount',
            field=models.DecimalField(blank=True, decimal_places=11, max_digits=19, null=True, verbose_name='Ratio to Buy'),
        ),
        migrations.AlterField(
            model_name='decisionsetting',
            name='ratio_to_buy',
            field=models.DecimalField(blank=True, decimal_places=11, max_digits=19, null=True, verbose_name='Ratio to Buy'),
        ),
        migrations.AlterField(
            model_name='decisionsetting',
            name='ratio_to_sell',
            field=models.DecimalField(decimal_places=11, max_digits=19, verbose_name='Ratio to Sell'),
        ),
    ]
