# Generated by Django 4.1.7 on 2023-03-10 07:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0003_house_house_view_list'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='house',
            name='house_view_list',
        ),
    ]