# Generated by Django 2.1.5 on 2020-01-09 15:52

import datetime
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
            name='Amenity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
                ('type', models.CharField(default='', max_length=255)),
                ('latitude', models.FloatField(default=0.0)),
                ('longitude', models.FloatField(default=0.0)),
                ('sid', models.CharField(default='', max_length=255)),
                ('classification', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Barangay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
                ('geojson', models.TextField(default='')),
                ('population', models.IntegerField(default=0)),
                ('income', models.FloatField(default=0.0)),
                ('latitude', models.FloatField(default=0.0)),
                ('longitude', models.FloatField(default=0.0)),
                ('spatial', models.FloatField(default=0.0)),
                ('temporal', models.FloatField(default=0.0)),
                ('economic', models.FloatField(default=0.0)),
                ('physical', models.FloatField(default=0.0)),
                ('psychological', models.FloatField(default=0.0)),
                ('physiological', models.FloatField(default=0.0)),
                ('sustainability', models.FloatField(default=0.0)),
                ('performance', models.FloatField(default=0.0)),
                ('fairness', models.FloatField(default=0.0)),
                ('sid', models.CharField(default='', max_length=255)),
                ('area', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
                ('is_active', models.BooleanField(default=False)),
                ('sid', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Coefficient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variable', models.CharField(default='', max_length=255)),
                ('coefficient', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Household',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission_id', models.CharField(default='', max_length=255)),
                ('submission_time', models.CharField(default='', max_length=255, null=True)),
                ('address', models.CharField(default='', max_length=255, null=True)),
                ('address_extra', models.TextField(default='', null=True)),
                ('income', models.FloatField(default=0.0)),
                ('education', models.CharField(default='', max_length=255)),
                ('num_cars', models.IntegerField(default=0)),
                ('years_residing', models.IntegerField(default=0)),
                ('own_or_rent', models.CharField(default='', max_length=255)),
                ('num_members', models.IntegerField(default=0)),
                ('barangay', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_console.Barangay')),
            ],
        ),
        migrations.CreateModel(
            name='HouseholdMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission_id', models.CharField(default='', max_length=255)),
                ('role', models.CharField(default='', max_length=255)),
                ('age', models.IntegerField(default=0)),
                ('occupation', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Indicator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
                ('description', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
                ('sid', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SurveyFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(max_length=500, null=True, upload_to='upload/survey/')),
                ('description', models.TextField(default='')),
                ('date_collected', models.DateField(default=datetime.date.today)),
                ('uploaded_by', models.DateTimeField(auto_now=True)),
                ('is_processed', models.BooleanField(default=False)),
                ('is_published', models.BooleanField(default=False)),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_console.City')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MainHouseholdMember',
            fields=[
                ('householdmember_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='admin_console.HouseholdMember')),
                ('job', models.CharField(default='', max_length=255, null=True)),
                ('income_range', models.CharField(default='', max_length=255)),
                ('trip_purpose', models.CharField(default='', max_length=255)),
                ('dest_address', models.CharField(default='', max_length=255, null=True)),
                ('dest_address_extra', models.TextField(default='', null=True)),
                ('trip_mode', models.CharField(default='', max_length=255)),
                ('travel_time', models.IntegerField(default=0)),
                ('gas_or_diesel', models.CharField(default='', max_length=255, null=True)),
                ('fuel_cost', models.FloatField(default=0.0)),
                ('fare', models.FloatField(default=0.0)),
                ('is_flood_prone', models.BooleanField(default=False)),
                ('will_cancel', models.BooleanField(default=False)),
                ('new_time', models.FloatField(default=0.0, null=True)),
                ('new_cost', models.FloatField(default=0.0, null=True)),
                ('travel_distance', models.FloatField(default=0.0, null=True)),
            ],
            bases=('admin_console.householdmember',),
        ),
        migrations.AddField(
            model_name='province',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_console.Region'),
        ),
        migrations.AddField(
            model_name='householdmember',
            name='household',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_console.Household'),
        ),
        migrations.AddField(
            model_name='household',
            name='survey_file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_console.SurveyFile'),
        ),
        migrations.AddField(
            model_name='coefficient',
            name='indicator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_console.Indicator'),
        ),
        migrations.AddField(
            model_name='city',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_console.Province'),
        ),
        migrations.AddField(
            model_name='barangay',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_console.City'),
        ),
        migrations.AddField(
            model_name='amenity',
            name='barangay',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_console.Barangay'),
        ),
        migrations.AddField(
            model_name='mainhouseholdmember',
            name='dest_barangay',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_console.Barangay'),
        ),
    ]
