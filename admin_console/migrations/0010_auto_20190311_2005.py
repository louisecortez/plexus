# Generated by Django 2.1.5 on 2019-03-11 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_console', '0009_amenities_osm_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Amenities',
            new_name='Amenity',
        ),
    ]