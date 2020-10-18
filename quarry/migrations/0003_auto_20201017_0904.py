# Generated by Django 3.1.2 on 2020-10-17 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quarry', '0002_quarry_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quarry',
            name='main_rock_type',
            field=models.CharField(choices=[('GRANITE', 'Granit/Granite'), ('LIMESTONE', 'Batu Kapur/Limestone'), ('QUARTZITE', 'Batu Kuartza/Quartzite'), ('SANDSTONE', 'Batu Pasir/Sandstone'), ('TUFF', 'Batu Tuf/tuff'), ('ANDESITE', 'Andesit/Andesite'), ('RHYOLITE', 'Ryolit/Rhyolite'), ('GRAVEL', 'Batu Kelikir/Gravel'), ('SERPENTINITE', 'Serpentinite'), ('GRANODIORITE', 'Granodiorite'), ('PERIDOTITE', 'Peridotite'), ('FELDSPAR', 'Feldspar'), ('DOLOMITE', 'Dolomite'), ('SHALE', 'Shale'), ('MICROTONALITE', 'Microtonalite'), ('GABBRO', 'Gabbro'), ('BASALT', 'Basalt'), ('HORNFELS', 'Hornfels'), ('DOLORITE', 'Dolorite'), ('DIORITE', 'Diorite')], max_length=255, verbose_name='jenis batuan utama'),
        ),
        migrations.AlterField(
            model_name='quarry',
            name='side_rock_type',
            field=models.CharField(blank=True, choices=[('GRANITE', 'Granit/Granite'), ('LIMESTONE', 'Batu Kapur/Limestone'), ('QUARTZITE', 'Batu Kuartza/Quartzite'), ('SANDSTONE', 'Batu Pasir/Sandstone'), ('TUFF', 'Batu Tuf/tuff'), ('ANDESITE', 'Andesit/Andesite'), ('RHYOLITE', 'Ryolit/Rhyolite'), ('GRAVEL', 'Batu Kelikir/Gravel'), ('SERPENTINITE', 'Serpentinite'), ('GRANODIORITE', 'Granodiorite'), ('PERIDOTITE', 'Peridotite'), ('FELDSPAR', 'Feldspar'), ('DOLOMITE', 'Dolomite'), ('SHALE', 'Shale'), ('MICROTONALITE', 'Microtonalite'), ('GABBRO', 'Gabbro'), ('BASALT', 'Basalt'), ('HORNFELS', 'Hornfels'), ('DOLORITE', 'Dolorite'), ('DIORITE', 'Diorite')], max_length=50, verbose_name='jenis batuan sampingan'),
        ),
    ]