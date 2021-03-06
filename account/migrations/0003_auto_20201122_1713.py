# Generated by Django 3.1.2 on 2020-11-22 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20201031_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='address1',
            field=models.CharField(max_length=255, verbose_name='alamat (No Rumah, Nama Jalan)'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='address2',
            field=models.CharField(blank=True, max_length=255, verbose_name='alamat (Daerah)'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='address3',
            field=models.CharField(blank=True, max_length=255, verbose_name='alamat (Poskod, Negeri)'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='ic_number',
            field=models.CharField(max_length=25, verbose_name='No Kad Pengenalan'),
        ),
    ]
