# Generated by Django 3.1.2 on 2020-10-31 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mine', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mine',
            name='company_category',
        ),
        migrations.RemoveField(
            model_name='mine',
            name='email',
        ),
        migrations.RemoveField(
            model_name='mine',
            name='fax_number',
        ),
        migrations.RemoveField(
            model_name='mine',
            name='max_capacity',
        ),
        migrations.RemoveField(
            model_name='mine',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='mine',
            name='method_mining',
            field=models.CharField(choices=[('DEDAH', 'Dedah'), ('BAWAH TANAH', 'Bawah Tanah'), ('KAPAL KOREK', 'Kapal Korek'), ('PAM KELIKIR', 'Pam Kelikir')], default='DEDAH', max_length=255, verbose_name='cara melombong'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mine',
            name='name',
            field=models.CharField(default='name', max_length=255, verbose_name='nama lombong'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mine',
            name='operator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mines', to='mine.operator', verbose_name='pengusaha'),
        ),
    ]
