# Generated by Django 2.1.5 on 2019-03-11 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_console', '0008_city_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='amenities',
            name='osm_id',
            field=models.IntegerField(default=0),
        ),
    ]