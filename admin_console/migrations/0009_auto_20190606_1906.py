# Generated by Django 2.1.5 on 2019-06-06 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_console', '0008_auto_20190606_1036'),
    ]

    operations = [
        migrations.RenameField(
            model_name='household',
            old_name='numCars',
            new_name='num_cars',
        ),
        migrations.RenameField(
            model_name='household',
            old_name='numMembers',
            new_name='num_members',
        ),
        migrations.RenameField(
            model_name='household',
            old_name='ownOrRent',
            new_name='own_or_rent',
        ),
        migrations.RenameField(
            model_name='household',
            old_name='surveyfile',
            new_name='survey_file',
        ),
        migrations.RenameField(
            model_name='household',
            old_name='yearsResiding',
            new_name='years_residing',
        ),
        migrations.AddField(
            model_name='household',
            name='extra_details',
            field=models.TextField(default='', null=True),
        ),
        migrations.AddField(
            model_name='surveyfile',
            name='is_processed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='household',
            name='address',
            field=models.CharField(default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='household',
            name='income',
            field=models.FloatField(default=0.0),
        ),
    ]
