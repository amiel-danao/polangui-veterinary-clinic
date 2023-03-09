# Generated by Django 4.0.4 on 2022-11-21 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_customuser_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='firstname',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='lastname',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='middlename',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
