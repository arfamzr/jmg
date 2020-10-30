# Generated by Django 3.1.2 on 2020-10-30 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mine', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='operator',
            name='state',
            field=models.CharField(choices=[('JHR', 'Johor'), ('KDH', 'Kedah'), ('KTN', 'Kelantan'), ('MLK', 'Melaka'), ('NSN', 'Negeri Sembilan'), ('PHG', 'Pahang'), ('PNG', 'Pulau Pinang'), ('PRK', 'Perak'), ('PLS', 'Perlis'), ('SBH', 'Sabah'), ('SWK', 'Sarawak'), ('SGR', 'Selangor'), ('TRG', 'Terengganu'), ('KUL', 'Kuala Lumpur'), ('LBN', 'Labuan'), ('PJY', 'Putrajaya')], default='KDH', max_length=3, verbose_name='negeri'),
            preserve_default=False,
        ),
    ]
