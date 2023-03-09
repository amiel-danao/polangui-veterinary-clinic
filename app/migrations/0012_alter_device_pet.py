# Generated by Django 4.0.4 on 2022-12-03 05:57

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_device_pet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='pet',
            field=smart_selects.db_fields.ChainedForeignKey(blank=True, chained_field='owner', chained_model_field='owner', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.pet'),
        ),
    ]
