# Generated by Django 3.1.2 on 2020-11-05 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quarry', '0002_auto_20201105_1231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salessubmission',
            name='amount',
            field=models.DecimalField(decimal_places=4, max_digits=15, verbose_name='amaun (Tan Metrik)'),
        ),
        migrations.AlterField(
            model_name='salessubmission',
            name='data',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_submissions', to='quarry.data', verbose_name='data'),
        ),
        migrations.AlterField(
            model_name='salessubmission',
            name='worth',
            field=models.DecimalField(decimal_places=2, max_digits=15, verbose_name='nilai (RM)'),
        ),
    ]