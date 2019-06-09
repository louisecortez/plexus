# Generated by Django 2.1.5 on 2019-06-06 02:14

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('admin_console', '0003_auto_20190606_1012'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(null=True, upload_to='surveys')),
                ('description', models.TextField(default='')),
                ('collected_by', models.DateField(default=datetime.date.today)),
                ('uploaded_by', models.DateTimeField(auto_now=True)),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_console.City')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]