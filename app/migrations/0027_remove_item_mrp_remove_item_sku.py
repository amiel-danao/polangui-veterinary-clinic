# Generated by Django 4.0.4 on 2023-08-21 00:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_remove_item_createdat_remove_item_createdby_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='mrp',
        ),
        migrations.RemoveField(
            model_name='item',
            name='sku',
        ),
    ]
