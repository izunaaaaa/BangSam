# Generated by Django 4.1.4 on 2023-03-02 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='keyword',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='house',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]