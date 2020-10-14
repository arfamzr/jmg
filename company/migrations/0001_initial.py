# Generated by Django 3.1.2 on 2020-10-13 11:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='nama syarikat')),
                ('address', models.CharField(max_length=255, verbose_name='alamat syarikat')),
                ('state', models.CharField(choices=[('JHR', 'Johor'), ('KDH', 'Kedah'), ('KTN', 'Kelantan'), ('MLK', 'Melaka'), ('NSN', 'Negeri Sembilan'), ('PHG', 'Pahang'), ('PNG', 'Pulau Pinang'), ('PRK', 'Perak'), ('PLS', 'Perlis'), ('SBH', 'Sabah'), ('SWK', 'Sarawak'), ('SGR', 'Selangor'), ('TRG', 'Terengganu'), ('KUL', 'Kuala Lumpur'), ('LBN', 'Labuan'), ('PJY', 'Putrajaya')], max_length=3, verbose_name='negeri')),
                ('phone', models.CharField(max_length=50, verbose_name='no phone')),
                ('fax', models.CharField(max_length=50, verbose_name='no fax')),
                ('email', models.CharField(max_length=255, verbose_name='emel')),
                ('status', models.BooleanField(default=True, verbose_name='status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'syarikat',
                'verbose_name_plural': 'syarikat',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('add_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees_added', to=settings.AUTH_USER_MODEL, verbose_name='add by')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', to='company.company', verbose_name='syarikat')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'pekerja',
                'verbose_name_plural': 'pekerja',
            },
        ),
    ]
