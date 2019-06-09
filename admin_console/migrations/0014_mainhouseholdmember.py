# Generated by Django 2.1.5 on 2019-06-08 07:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_console', '0013_auto_20190608_1550'),
    ]

    operations = [
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
                ('dest_barangay', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_console.Barangay')),
            ],
            bases=('admin_console.householdmember',),
        ),
    ]