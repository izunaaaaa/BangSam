# Generated by Django 4.0.10 on 2023-03-23 06:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0011_remove_house_distance_to_station'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='options',
            new_name='Option',
        ),
        migrations.RenameModel(
            old_name='safetyoptions',
            new_name='Safetyoption',
        ),
        migrations.RenameField(
            model_name='option',
            old_name='option',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='safetyoption',
            old_name='safetyoption',
            new_name='name',
        ),
    ]
