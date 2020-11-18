# Generated by Django 3.1.2 on 2020-11-16 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quarry', '0003_auto_20201106_0013'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leaseholder',
            name='lease_expired',
        ),
        migrations.AlterField(
            model_name='leaseholder',
            name='lease_number',
            field=models.CharField(max_length=255, verbose_name='No Hakmilik / No Lot'),
        ),
    ]
