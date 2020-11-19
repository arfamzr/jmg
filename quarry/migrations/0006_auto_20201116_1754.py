# Generated by Django 3.1.2 on 2020-11-16 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quarry', '0005_auto_20201116_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='salessubmission',
            name='total',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=15, verbose_name='Jumlah (RM)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='salessubmission',
            name='worth',
            field=models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Nilai (RM) / Tan Matrik'),
        ),
    ]