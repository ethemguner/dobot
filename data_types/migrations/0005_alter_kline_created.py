# Generated by Django 3.2.9 on 2021-11-19 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_types', '0004_auto_20211119_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kline',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
