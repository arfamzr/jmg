# Generated by Django 3.1.2 on 2021-01-16 21:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import quarry.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0003_auto_20201122_1713'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcessData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(choices=[('JHR', 'Johor'), ('KDH', 'Kedah'), ('KTN', 'Kelantan'), ('MLK', 'Melaka'), ('NSN', 'Negeri Sembilan'), ('PHG', 'Pahang'), ('PNG', 'Pulau Pinang'), ('PRK', 'Perak'), ('PLS', 'Perlis'), ('SBH', 'Sabah'), ('SWK', 'Sarawak'), ('SGR', 'Selangor'), ('TRG', 'Terengganu'), ('KUL', 'Kuala Lumpur'), ('LBN', 'Labuan'), ('PJY', 'Putrajaya')], max_length=3, verbose_name='negeri')),
                ('month', models.PositiveIntegerField(choices=[(1, 'Januari'), (2, 'Februari'), (3, 'Mac'), (4, 'April'), (5, 'Mei'), (6, 'Jun'), (7, 'Julai'), (8, 'Ogos'), (9, 'September'), (10, 'Oktober'), (11, 'November'), (12, 'Disember')], verbose_name='bulan')),
                ('year', models.PositiveIntegerField(choices=[(2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021)], default=quarry.models.current_year, verbose_name='tahun')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'data lesen memproses',
                'verbose_name_plural': 'data lesen memproses',
            },
        ),
        migrations.CreateModel(
            name='ProcessFactory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='nama')),
                ('license_no', models.CharField(max_length=255, verbose_name='no. lesen memproses mineral')),
                ('state', models.CharField(choices=[('JHR', 'Johor'), ('KDH', 'Kedah'), ('KTN', 'Kelantan'), ('MLK', 'Melaka'), ('NSN', 'Negeri Sembilan'), ('PHG', 'Pahang'), ('PNG', 'Pulau Pinang'), ('PRK', 'Perak'), ('PLS', 'Perlis'), ('SBH', 'Sabah'), ('SWK', 'Sarawak'), ('SGR', 'Selangor'), ('TRG', 'Terengganu'), ('KUL', 'Kuala Lumpur'), ('LBN', 'Labuan'), ('PJY', 'Putrajaya')], max_length=3, verbose_name='negeri')),
                ('status', models.BooleanField(default=True, verbose_name='status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'kilang proses',
                'verbose_name_plural': 'kilang proses',
            },
        ),
        migrations.CreateModel(
            name='ElectricMachinery',
            fields=[
                ('data', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='mineral.processdata', verbose_name='data')),
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
                ('data', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='mineral.processdata', verbose_name='data')),
                ('total_diesel', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='jumlah diesel')),
                ('total_electric', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='jumlah elektrik')),
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
                ('data', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='mineral.processdata', verbose_name='data')),
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
                ('data', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='mineral.processdata', verbose_name='data')),
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
                ('data', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='mineral.processdata', verbose_name='data')),
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
                ('data', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='mineral.processdata', verbose_name='data')),
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
                ('data', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='mineral.processdata', verbose_name='data')),
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
                ('total_male', models.IntegerField(verbose_name='jumlah lelaki')),
                ('total_female', models.IntegerField(verbose_name='jumlah perempuan')),
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
                ('data', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='mineral.processdata', verbose_name='data')),
                ('operating_hours', models.IntegerField(verbose_name='jam operasi sehari')),
                ('operating_days', models.IntegerField(verbose_name='bilangan hari operasi')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'rekod operasi',
                'verbose_name_plural': 'rekod operasi',
            },
        ),
        migrations.CreateModel(
            name='ProcessSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mineral_type', models.CharField(choices=[('BAUXITE', 'Bauksite/Bauksit'), ('TIN ORE', 'Tin Ore/Bijih Timah'), ('IRON ORE', 'Iron Ore/Bijih Besi'), ('ANTIMONY', 'Antimony/Antimoni'), ('COAL', 'Coal/Arang Batu'), ('DIMENSION STONE', 'Dimension Stone/Batu Dimensi'), ('FELDSPAR', 'Feldspar/Felspar'), ('GALENA', 'Galena/Galena'), ('BATU KAPUR', 'Limestone/Batu Kapur'), ('KAOLIN', 'Kaolin'), ('CUPRUM', 'Kuprum'), ('BALL CLAY', 'Ball Clay/Lempung Bebola'), ('MANGANESE', 'Manganese/Mangan'), ('MICA', 'Mica/Mika'), ('SILVER', 'Silver/Perak'), ('SILICA SAND', 'Silica Sand/Pasir Silika'), ('TUNGSTEN', 'Tungsten'), ('GOLD', 'Gold/Emas'), ('GRAPHITE', 'Graphite/Grafit')], max_length=255, verbose_name='jenis mineral utama')),
                ('quantity_unit', models.CharField(choices=[('KG', 'Kilogram'), ('M3', 'Meter Persegi'), ('GRAM', 'Gram'), ('TAN', 'Tan')], default='TAN', max_length=255, verbose_name='unit kuantiti')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='kuantiti')),
                ('buyer', models.CharField(max_length=255, verbose_name='pembeli')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submission', to='mineral.processdata', verbose_name='data')),
            ],
            options={
                'verbose_name': 'statistic lesen process',
                'verbose_name_plural': 'statistic lesen process',
            },
        ),
        migrations.CreateModel(
            name='ProcessStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mineral_type', models.CharField(choices=[('BAUXITE', 'Bauksite/Bauksit'), ('TIN ORE', 'Tin Ore/Bijih Timah'), ('IRON ORE', 'Iron Ore/Bijih Besi'), ('ANTIMONY', 'Antimony/Antimoni'), ('COAL', 'Coal/Arang Batu'), ('DIMENSION STONE', 'Dimension Stone/Batu Dimensi'), ('FELDSPAR', 'Feldspar/Felspar'), ('GALENA', 'Galena/Galena'), ('BATU KAPUR', 'Limestone/Batu Kapur'), ('KAOLIN', 'Kaolin'), ('CUPRUM', 'Kuprum'), ('BALL CLAY', 'Ball Clay/Lempung Bebola'), ('MANGANESE', 'Manganese/Mangan'), ('MICA', 'Mica/Mika'), ('SILVER', 'Silver/Perak'), ('SILICA SAND', 'Silica Sand/Pasir Silika'), ('TUNGSTEN', 'Tungsten'), ('GOLD', 'Gold/Emas'), ('GRAPHITE', 'Graphite/Grafit')], max_length=255, verbose_name='jenis mineral utama')),
                ('quantity_unit', models.CharField(choices=[('KG', 'Kilogram'), ('M3', 'Meter Persegi'), ('GRAM', 'Gram'), ('TAN', 'Tan')], default='TAN', max_length=255, verbose_name='unit kuantiti')),
                ('initial_stock', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='stok awal bulan')),
                ('external_sources', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='pembelian dari punca luar')),
                ('production', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='pengeluaran')),
                ('total', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='jumlah')),
                ('sold', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='penjualan')),
                ('final_stock', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='stock akhir bulan')),
                ('mineral_gred', models.CharField(max_length=50, verbose_name='gred mineral')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statistics', to='mineral.processdata', verbose_name='data')),
            ],
            options={
                'verbose_name': 'statistik lesen proses',
                'verbose_name_plural': 'statistik lesen proses',
            },
        ),
        migrations.CreateModel(
            name='ProcessManager',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='account.user', verbose_name='user')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('factory', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mineral.processfactory', verbose_name='kilang')),
            ],
            options={
                'verbose_name': 'pengurus lesen memproses',
                'verbose_name_plural': 'pengurus lesen memproses',
            },
        ),
        migrations.AddField(
            model_name='processdata',
            name='factory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='data', to='mineral.processfactory', verbose_name='kilang'),
        ),
        migrations.AddField(
            model_name='processdata',
            name='manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='process_data', to='mineral.processmanager', verbose_name='pengurus'),
        ),
        migrations.CreateModel(
            name='Other',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='tajuk')),
                ('comment', models.TextField(blank=True, verbose_name='komen')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='others', to='mineral.processdata', verbose_name='data')),
            ],
            options={
                'verbose_name': 'lain-lain',
                'verbose_name_plural': 'lain-lain',
            },
        ),
        migrations.CreateModel(
            name='Approval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state_comment', models.TextField(blank=True, verbose_name='state comment')),
                ('state_approved', models.BooleanField(blank=True, null=True, verbose_name='state approved')),
                ('admin_comment', models.TextField(blank=True, verbose_name='admin comment')),
                ('admin_approved', models.BooleanField(blank=True, null=True, verbose_name='admin approved')),
                ('hq_comment', models.TextField(blank=True, verbose_name='hq comment')),
                ('hq_approved', models.BooleanField(blank=True, null=True, verbose_name='hq approved')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('admin_inspector', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='process_admin_inspected', to=settings.AUTH_USER_MODEL, verbose_name='admin inspector')),
                ('data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approvals', to='mineral.processdata', verbose_name='data')),
                ('hq_inspector', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='process_hq_inspected', to=settings.AUTH_USER_MODEL, verbose_name='hq inspector')),
                ('requestor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='process_requested', to=settings.AUTH_USER_MODEL, verbose_name='requestor')),
                ('state_inspector', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='process_state_inspected', to=settings.AUTH_USER_MODEL, verbose_name='state inspector')),
            ],
        ),
    ]
