# Generated by Django 4.0.4 on 2022-12-19 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_immunizationhistory_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='immunizationhistory',
            name='veterinarian',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
