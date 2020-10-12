# Generated by Django 3.1.2 on 2020-10-06 16:36

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
            name='Mine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, verbose_name='kod')),
                ('location', models.CharField(max_length=255, verbose_name='kawasan')),
                ('main_mineral', models.CharField(max_length=255, verbose_name='mineral utama')),
                ('mine_technique', models.CharField(max_length=255, verbose_name='cara melombong')),
                ('category', models.CharField(max_length=255, verbose_name='kategori')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'lombong',
                'verbose_name_plural': 'lombong',
            },
        ),
        migrations.CreateModel(
            name='ElectricMachinery',
            fields=[
                ('mine', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='mine.mine', verbose_name='kuari')),
                ('number_lorry', models.IntegerField(verbose_name='bilangan lori')),
                ('lorry_power', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='kuasa lori')),
                ('number_excavator', models.IntegerField(verbose_name='bilangan jenkorek')),
                ('excavator_power', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='kuasa jenkorek')),
                ('number_wheel_loader', models.IntegerField(verbose_name='bilangan jentera angkut beroda')),
                ('wheel_loader_power', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='kuasa jentera angkut beroda')),
                ('number_bulldozer', models.IntegerField(verbose_name='bilangan jentolak')),
                ('bulldozer_power', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='kuasa jentolak')),
                ('number_water_pump', models.IntegerField(verbose_name='bilangan pam air')),
                ('water_pump_power', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='kuasa pam air')),
                ('number_air_compressor', models.IntegerField(verbose_name='bilangan pemampat udara')),
                ('air_compressor_power', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='kuasa pemampat udara')),
                ('number_hydraulic_breaker', models.IntegerField(verbose_name='bilangan pemecah hidraulik')),
                ('hydraulic_breaker_power', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='kuasa pemecah hidraulik')),
                ('number_hydraulic_drill', models.IntegerField(verbose_name='bilangan gerudi hidraulik')),
                ('hydraulic_drill_power', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='kuasa gerudi hidraulik')),
                ('number_crusher', models.IntegerField(verbose_name='bilangan penghancur')),
                ('crusher_power', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='kuasa penghancur')),
                ('number_shovel', models.IntegerField(verbose_name='bilangan penyuduk')),
                ('shovel_power', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='kuasa penyuduk')),
                ('number_tracktor', models.IntegerField(verbose_name='bilangan traktor')),
                ('tracktor_power', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='kuasa traktor')),
                ('number_other', models.IntegerField(verbose_name='bilangan lain')),
                ('other_power', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='kuasa lain')),
                ('state_other', models.TextField(blank=True, verbose_name='nyatakan lain')),
                ('total_number', models.IntegerField(verbose_name='jumlah bilangan')),
                ('total_power', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='jumlah_kuasa')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'jentera elektrik',
                'verbose_name_plural': 'jentera elektrik',
            },
        ),
        migrations.CreateModel(
            name='EnergySupply',
            fields=[
                ('mine', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='mine.mine', verbose_name='kuari')),
                ('total_diesel', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='jumlah diesel')),
                ('total_electric', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='jumlah elektrik')),
                ('total_explosive', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='jumlah bahan letupan')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'bahan tenaga',
                'verbose_name_plural': 'bahan tenaga',
            },
        ),
        migrations.CreateModel(
            name='ForeignContractor',
            fields=[
                ('mine', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='mine.mine', verbose_name='kuari')),
                ('male_manager', models.IntegerField(verbose_name='pengurus lelaki')),
                ('female_manager', models.IntegerField(verbose_name='pengurus perempuan')),
                ('male_professional', models.IntegerField(verbose_name='profesional lelaki')),
                ('female_professional', models.IntegerField(verbose_name='profesional perempuan')),
                ('male_technical', models.IntegerField(verbose_name='teknikal lelaki')),
                ('female_technical', models.IntegerField(verbose_name='teknikal perempuan')),
                ('male_clerk', models.IntegerField(verbose_name='kerani lelaki')),
                ('female_clerk', models.IntegerField(verbose_name='kerani perempuan')),
                ('male_labor', models.IntegerField(verbose_name='buruh lelaki')),
                ('female_labor', models.IntegerField(verbose_name='buruh perempuan')),
                ('total_female', models.IntegerField(verbose_name='jumlah perempuan')),
                ('total_male', models.IntegerField(verbose_name='jumlah lelaki')),
                ('total_male_salary', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='jumlah upah gaji lelaki')),
                ('total_female_salary', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='jumlah upah gaji perempuan')),
                ('male_man_hour', models.IntegerField(verbose_name='jam manusia lelaki')),
                ('female_man_hour', models.IntegerField(verbose_name='jam manusia perempuan')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'kontraktor asing',
                'verbose_name_plural': 'kontraktor asing',
            },
        ),
        migrations.CreateModel(
            name='ForeignOperator',
            fields=[
                ('mine', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='mine.mine', verbose_name='kuari')),
                ('male_manager', models.IntegerField(verbose_name='pengurus lelaki')),
                ('female_manager', models.IntegerField(verbose_name='pengurus perempuan')),
                ('male_professional', models.IntegerField(verbose_name='profesional lelaki')),
                ('female_professional', models.IntegerField(verbose_name='profesional perempuan')),
                ('male_technical', models.IntegerField(verbose_name='teknikal lelaki')),
                ('female_technical', models.IntegerField(verbose_name='teknikal perempuan')),
                ('male_clerk', models.IntegerField(verbose_name='kerani lelaki')),
                ('female_clerk', models.IntegerField(verbose_name='kerani perempuan')),
                ('male_labor', models.IntegerField(verbose_name='buruh lelaki')),
                ('female_labor', models.IntegerField(verbose_name='buruh perempuan')),
                ('total_female', models.IntegerField(verbose_name='jumlah perempuan')),
                ('total_male', models.IntegerField(verbose_name='jumlah lelaki')),
                ('total_male_salary', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='jumlah upah gaji lelaki')),
                ('total_female_salary', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='jumlah upah gaji perempuan')),
                ('male_man_hour', models.IntegerField(verbose_name='jam manusia lelaki')),
                ('female_man_hour', models.IntegerField(verbose_name='jam manusia perempuan')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'operator asing',
                'verbose_name_plural': 'operator asing',
            },
        ),
        migrations.CreateModel(
            name='InternalCombustionMachinery',
            fields=[
                ('mine', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='mine.mine', verbose_name='kuari')),
                ('number_lorry', models.IntegerField(verbose_name='bilangan lori')),
                ('lorry_power', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='kuasa lori')),
                ('number_excavator', models.IntegerField(verbose_name='bilangan jenkorek')),
                ('excavator_power', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='kuasa jenkorek')),
                ('number_wheel_loader', models.IntegerField(verbose_name='bilangan jentera angkut beroda')),
                ('wheel_loader_power', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='kuasa jentera angkut beroda')),
                ('number_bulldozer', models.IntegerField(verbose_name='bilangan jentolak')),
                ('bulldozer_power', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='kuasa jentolak')),
                ('number_water_pump', models.IntegerField(verbose_name='bilangan pam air')),
                ('water_pump_power', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='kuasa pam air')),
                ('number_air_compressor', models.IntegerField(verbose_name='bilangan pemampat udara')),
                ('air_compressor_power', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='kuasa pemampat udara')),
                ('number_hydraulic_breaker', models.IntegerField(verbose_name='bilangan pemecah hidraulik')),
                ('hydraulic_breaker_power', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='kuasa pemecah hidraulik')),
                ('number_hydraulic_drill', models.IntegerField(verbose_name='bilangan gerudi hidraulik')),
                ('hydraulic_drill_power', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='kuasa gerudi hidraulik')),
                ('number_crusher', models.IntegerField(verbose_name='bilangan penghancur')),
                ('crusher_power', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='kuasa penghancur')),
                ('number_shovel', models.IntegerField(verbose_name='bilangan penyuduk')),
                ('shovel_power', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='kuasa penyuduk')),
                ('number_tracktor', models.IntegerField(verbose_name='bilangan traktor')),
                ('tracktor_power', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='kuasa traktor')),
                ('number_other', models.IntegerField(verbose_name='bilangan lain')),
                ('other_power', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='kuasa lain')),
                ('state_other', models.TextField(blank=True, verbose_name='nyatakan lain')),
                ('total_number', models.IntegerField(verbose_name='jumlah bilangan')),
                ('total_power', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='jumlah_kuasa')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'jentera bakar dalam',
                'verbose_name_plural': 'jentera bakar dalam',
            },
        ),
        migrations.CreateModel(
            name='LocalContractor',
            fields=[
                ('mine', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='mine.mine', verbose_name='kuari')),
                ('male_manager', models.IntegerField(verbose_name='pengurus lelaki')),
                ('female_manager', models.IntegerField(verbose_name='pengurus perempuan')),
                ('male_professional', models.IntegerField(verbose_name='profesional lelaki')),
                ('female_professional', models.IntegerField(verbose_name='profesional perempuan')),
                ('male_technical', models.IntegerField(verbose_name='teknikal lelaki')),
                ('female_technical', models.IntegerField(verbose_name='teknikal perempuan')),
                ('male_clerk', models.IntegerField(verbose_name='kerani lelaki')),
                ('female_clerk', models.IntegerField(verbose_name='kerani perempuan')),
                ('male_labor', models.IntegerField(verbose_name='buruh lelaki')),
                ('female_labor', models.IntegerField(verbose_name='buruh perempuan')),
                ('total_female', models.IntegerField(verbose_name='jumlah perempuan')),
                ('total_male', models.IntegerField(verbose_name='jumlah lelaki')),
                ('total_male_salary', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='jumlah upah gaji lelaki')),
                ('total_female_salary', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='jumlah upah gaji perempuan')),
                ('male_man_hour', models.IntegerField(verbose_name='jam manusia lelaki')),
                ('female_man_hour', models.IntegerField(verbose_name='jam manusia perempuan')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'kontraktor tempatan',
                'verbose_name_plural': 'kontraktor tempatan',
            },
        ),
        migrations.CreateModel(
            name='LocalOperator',
            fields=[
                ('mine', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='mine.mine', verbose_name='kuari')),
                ('male_manager', models.IntegerField(verbose_name='pengurus lelaki')),
                ('female_manager', models.IntegerField(verbose_name='pengurus perempuan')),
                ('male_professional', models.IntegerField(verbose_name='profesional lelaki')),
                ('female_professional', models.IntegerField(verbose_name='profesional perempuan')),
                ('male_technical', models.IntegerField(verbose_name='teknikal lelaki')),
                ('female_technical', models.IntegerField(verbose_name='teknikal perempuan')),
                ('male_clerk', models.IntegerField(verbose_name='kerani lelaki')),
                ('female_clerk', models.IntegerField(verbose_name='kerani perempuan')),
                ('male_labor', models.IntegerField(verbose_name='buruh lelaki')),
                ('female_labor', models.IntegerField(verbose_name='buruh perempuan')),
                ('total_female', models.IntegerField(verbose_name='jumlah perempuan')),
                ('total_male', models.IntegerField(verbose_name='jumlah lelaki')),
                ('total_male_salary', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='jumlah upah gaji lelaki')),
                ('total_female_salary', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='jumlah upah gaji perempuan')),
                ('male_man_hour', models.IntegerField(verbose_name='jam manusia lelaki')),
                ('female_man_hour', models.IntegerField(verbose_name='jam manusia perempuan')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'operator tempatan',
                'verbose_name_plural': 'operator tempatan',
            },
        ),
        migrations.CreateModel(
            name='OperatingRecord',
            fields=[
                ('mine', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='mine.mine', verbose_name='kuari')),
                ('average_mine_depth', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='dalam lombong hitung panjang')),
                ('deepest_mine', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='ukuran lombong terdalam')),
                ('shallowest_mine', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='ukuran lombong tercetek')),
                ('material_discarded', models.DecimalField(decimal_places=4, max_digits=15, verbose_name='bahan beban dibuang')),
                ('ore_mined', models.DecimalField(decimal_places=4, max_digits=15, verbose_name='bahan berbijih dilombong')),
            ],
            options={
                'verbose_name': 'rekod operasi',
                'verbose_name_plural': 'rekod operasi',
            },
        ),
        migrations.CreateModel(
            name='Statistic',
            fields=[
                ('mine', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='mine.mine', verbose_name='lombong')),
                ('minerals_quantity', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='kuantiti_mineral')),
                ('final_stock_last_month', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='stok akhir bulan lalu')),
                ('mine_production', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='pengeluaran lombong')),
                ('total_minerals', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='jumlah mineral')),
                ('submission_buyers', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='penyerahan kepada pembeli')),
                ('final_stock_this_month', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='stok akhir bulan ini')),
                ('average_grade', models.CharField(max_length=255, verbose_name='gred hitung panjang')),
            ],
            options={
                'verbose_name': 'perangkaan',
                'verbose_name_plural': 'perangkaan',
            },
        ),
    ]