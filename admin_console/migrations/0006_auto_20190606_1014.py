# Generated by Django 2.1.5 on 2019-06-06 02:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_console', '0005_auto_20190606_1014'),
    ]

    operations = [
        migrations.RenameField(
            model_name='household',
            old_name='datafile',
            new_name='surveyfile',
        ),
    ]
