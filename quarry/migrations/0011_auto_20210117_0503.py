# Generated by Django 3.1.2 on 2021-01-16 21:03

from django.db import migrations, models
import quarry.models


class Migration(migrations.Migration):

    dependencies = [
        ('quarry', '0010_auto_20201122_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='year',
            field=models.PositiveIntegerField(choices=[(2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021)], default=quarry.models.current_year, verbose_name='tahun'),
        ),
    ]
