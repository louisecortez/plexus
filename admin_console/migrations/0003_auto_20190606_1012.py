# Generated by Django 2.1.5 on 2019-06-06 02:12

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('admin_console', '0002_amenity_classification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datafile',
            name='name',
        ),
        migrations.AddField(
            model_name='datafile',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_console.City'),
        ),
        migrations.AddField(
            model_name='datafile',
            name='collected_by',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='datafile',
            name='file',
            field=models.FileField(null=True, upload_to='surveys'),
        ),
        migrations.AddField(
            model_name='datafile',
            name='uploaded_by',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='datafile',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
