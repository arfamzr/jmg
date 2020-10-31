# Generated by Django 3.1.2 on 2020-10-31 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='address1',
            field=models.CharField(default='address1', max_length=255, verbose_name='alamat'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='address2',
            field=models.CharField(blank=True, max_length=255, verbose_name='alamat (line 2)'),
        ),
        migrations.AddField(
            model_name='profile',
            name='address3',
            field=models.CharField(blank=True, max_length=255, verbose_name='alamat (line 3)'),
        ),
        migrations.AddField(
            model_name='profile',
            name='ic_number',
            field=models.CharField(default='ic number', max_length=25, verbose_name='no K/P'),
            preserve_default=False,
        ),
    ]
