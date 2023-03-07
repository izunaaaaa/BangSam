# Generated by Django 4.1.7 on 2023-03-07 05:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_alter_review_house_rating_alter_review_user_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='house_rating',
            field=models.PositiveIntegerField(blank=True, default=0, help_text='0~5사이 값으로 입력하세요', null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='review',
            name='user_rating',
            field=models.PositiveIntegerField(blank=True, default=0, help_text='0~5사이 값으로 입력하세요', null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
