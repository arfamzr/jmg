# Generated by Django 3.1.2 on 2020-10-28 17:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mine', '0004_auto_20201028_1637'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mineral_type', models.CharField(choices=[('BAUXITE', 'Bauksite/Bauksit'), ('TIN ORE', 'Tin Ore/Bijih Timah'), ('IRON ORE', 'Iron Ore/Bijih Besi'), ('ANTIMONY', 'Antimony/Antimoni'), ('COAL', 'Coal/Arang Batu'), ('DIMENSION STONE', 'Dimension Stone/Batu Dimensi'), ('FELDSPAR', 'Feldspar/Felspar'), ('GALENA', 'Galena/Galena'), ('KALSIUM KARBONAT', 'Kalsium Karbonat'), ('KAOLIN', 'Kaolin'), ('CUPRUM', 'Kuprum'), ('BALL CLAY', 'Ball Clay/Lempung Bebola'), ('MANGANESE', 'Manganese/Mangan'), ('MICA', 'Mica/Mika'), ('SILVER', 'Silver/Perak'), ('SILICA SAND', 'Silica Sand/Pasir Silika'), ('TUNGSTEN', 'Tungsten'), ('GOLD', 'Gold/Emas'), ('GRAPHITE', 'Graphite/Grafit')], max_length=255, verbose_name='jenis mineral utama')),
                ('minerals_quantity', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='kuantiti_mineral')),
                ('final_stock_last_month', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='stok akhir bulan lalu')),
                ('mine_production', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='pengeluaran lombong')),
                ('total_minerals', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='jumlah mineral')),
                ('submission_buyers', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='penyerahan kepada pembeli')),
                ('final_stock_this_month', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='stok akhir bulan ini')),
                ('average_grade', models.CharField(max_length=255, verbose_name='gred hitung panjang')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('miner_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_minerals', to='mine.mineminerdata', verbose_name='miner data')),
            ],
            options={
                'verbose_name': 'perangkaan batuan utama',
                'verbose_name_plural': 'perangkaan batuan utama',
            },
        ),
        migrations.CreateModel(
            name='SideStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mineral_type', models.CharField(choices=[('BAUXITE', 'Bauksite/Bauksit'), ('TIN ORE', 'Tin Ore/Bijih Timah'), ('IRON ORE', 'Iron Ore/Bijih Besi'), ('ANTIMONY', 'Antimony/Antimoni'), ('COAL', 'Coal/Arang Batu'), ('DIMENSION STONE', 'Dimension Stone/Batu Dimensi'), ('FELDSPAR', 'Feldspar/Felspar'), ('GALENA', 'Galena/Galena'), ('KALSIUM KARBONAT', 'Kalsium Karbonat'), ('KAOLIN', 'Kaolin'), ('CUPRUM', 'Kuprum'), ('BALL CLAY', 'Ball Clay/Lempung Bebola'), ('MANGANESE', 'Manganese/Mangan'), ('MICA', 'Mica/Mika'), ('SILVER', 'Silver/Perak'), ('SILICA SAND', 'Silica Sand/Pasir Silika'), ('TUNGSTEN', 'Tungsten'), ('GOLD', 'Gold/Emas'), ('GRAPHITE', 'Graphite/Grafit')], max_length=255, verbose_name='jenis mineral sampingan')),
                ('minerals_quantity', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='kuantiti_mineral')),
                ('final_stock_last_month', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='stok akhir bulan lalu')),
                ('mine_production', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='pengeluaran lombong')),
                ('total_minerals', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='jumlah mineral')),
                ('submission_buyers', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='penyerahan kepada pembeli')),
                ('final_stock_this_month', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='stok akhir bulan ini')),
                ('average_grade', models.CharField(max_length=255, verbose_name='gred hitung panjang')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('miner_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='side_minerals', to='mine.mineminerdata', verbose_name='miner data')),
            ],
            options={
                'verbose_name': 'perangkaan batuan sampingan',
                'verbose_name_plural': 'perangkaan batuan sampingan',
            },
        ),
        migrations.RemoveField(
            model_name='mine',
            name='main_mineral_type',
        ),
        migrations.RemoveField(
            model_name='mine',
            name='side_mineral_type',
        ),
        migrations.DeleteModel(
            name='Statistic',
        ),
    ]