# Generated by Django 3.1.2 on 2020-10-06 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quarry', '0007_auto_20201006_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='electricmachinery',
            name='state_other',
            field=models.TextField(blank=True, verbose_name='nyatakan lain'),
        ),
        migrations.AlterField(
            model_name='exportfinaluses',
            name='state_other',
            field=models.TextField(blank=True, verbose_name='nyatakan lain'),
        ),
        migrations.AlterField(
            model_name='internalcombustionmachinery',
            name='state_other',
            field=models.TextField(blank=True, verbose_name='nyatakan lain'),
        ),
        migrations.AlterField(
            model_name='localfinaluses',
            name='state_other',
            field=models.TextField(blank=True, verbose_name='nyatakan lain'),
        ),
    ]
