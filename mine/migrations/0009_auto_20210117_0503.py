# Generated by Django 3.1.2 on 2021-01-16 21:03

from django.db import migrations, models
import quarry.models


class Migration(migrations.Migration):

    dependencies = [
        ('mine', '0008_auto_20201121_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='year',
            field=models.PositiveIntegerField(choices=[(2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021)], default=quarry.models.current_year, verbose_name='tahun'),
        ),
    ]
