# Generated by Django 3.1.2 on 2020-10-28 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mine', '0003_auto_20201017_0904'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mine',
            name='main_rock_type',
        ),
        migrations.RemoveField(
            model_name='mine',
            name='side_rock_type',
        ),
        migrations.AddField(
            model_name='mine',
            name='main_mineral_type',
            field=models.CharField(choices=[('GRANITE', 'Granit/Granite'), ('LIMESTONE', 'Batu Kapur/Limestone'), ('QUARTZITE', 'Batu Kuartza/Quartzite'), ('SANDSTONE', 'Batu Pasir/Sandstone'), ('TUFF', 'Batu Tuf/tuff'), ('ANDESITE', 'Andesit/Andesite'), ('RHYOLITE', 'Ryolit/Rhyolite'), ('GRAVEL', 'Batu Kelikir/Gravel'), ('SERPENTINITE', 'Serpentinite'), ('GRANODIORITE', 'Granodiorite'), ('PERIDOTITE', 'Peridotite'), ('FELDSPAR', 'Feldspar'), ('DOLOMITE', 'Dolomite'), ('SHALE', 'Shale'), ('MICROTONALITE', 'Microtonalite'), ('GABBRO', 'Gabbro'), ('BASALT', 'Basalt'), ('HORNFELS', 'Hornfels'), ('DOLORITE', 'Dolorite'), ('DIORITE', 'Diorite')], default='GOLD', max_length=255, verbose_name='jenis mineral utama'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mine',
            name='side_mineral_type',
            field=models.CharField(blank=True, choices=[('GRANITE', 'Granit/Granite'), ('LIMESTONE', 'Batu Kapur/Limestone'), ('QUARTZITE', 'Batu Kuartza/Quartzite'), ('SANDSTONE', 'Batu Pasir/Sandstone'), ('TUFF', 'Batu Tuf/tuff'), ('ANDESITE', 'Andesit/Andesite'), ('RHYOLITE', 'Ryolit/Rhyolite'), ('GRAVEL', 'Batu Kelikir/Gravel'), ('SERPENTINITE', 'Serpentinite'), ('GRANODIORITE', 'Granodiorite'), ('PERIDOTITE', 'Peridotite'), ('FELDSPAR', 'Feldspar'), ('DOLOMITE', 'Dolomite'), ('SHALE', 'Shale'), ('MICROTONALITE', 'Microtonalite'), ('GABBRO', 'Gabbro'), ('BASALT', 'Basalt'), ('HORNFELS', 'Hornfels'), ('DOLORITE', 'Dolorite'), ('DIORITE', 'Diorite')], max_length=255, verbose_name='jenis mineral sampingan'),
        ),
    ]