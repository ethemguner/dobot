# Generated by Django 3.2.9 on 2022-01-02 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coins', '0011_auto_20211218_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coin',
            name='symbol',
            field=models.CharField(choices=[('BTCUSDT', 'Bitcoin/USD'), ('ETHUSDT', 'Etherium/USD'), ('BNBUSDT', 'Binance Coin/USD'), ('ADAUSDT', 'Cardano/USD'), ('ADAUSDT', 'ShibaInu/USD')], max_length=50, verbose_name='Symbol'),
        ),
    ]
