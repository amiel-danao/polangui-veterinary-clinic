# Generated by Django 4.0.4 on 2023-01-27 14:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_alter_immunizationhistory_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='immunizationhistory',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='immunizationhistory',
            name='dose',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AddField(
            model_name='immunizationhistory',
            name='owner_actions',
            field=models.CharField(default='None', max_length=255),
        ),
        migrations.AddField(
            model_name='immunizationhistory',
            name='veterinary_actions',
            field=models.CharField(default='None', max_length=255),
        ),
        migrations.AlterUniqueTogether(
            name='immunizationhistory',
            unique_together={('pet', 'pet_age', 'vaccine', 'dose')},
        ),
        migrations.RemoveField(
            model_name='immunizationhistory',
            name='next_vaccination_date',
        ),
    ]
