# Generated by Django 4.1.7 on 2023-03-11 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('houselists', '0001_initial'),
        ('houses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='houselist',
            name='recently_views',
            field=models.ManyToManyField(to='houses.house'),
        ),
    ]