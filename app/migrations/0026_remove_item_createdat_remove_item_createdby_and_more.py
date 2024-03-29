# Generated by Django 4.0.4 on 2023-08-21 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_alter_appointment_payment_method_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='createdat',
        ),
        migrations.RemoveField(
            model_name='item',
            name='createdby',
        ),
        migrations.RemoveField(
            model_name='item',
            name='orderid',
        ),
        migrations.RemoveField(
            model_name='item',
            name='supplierid',
        ),
        migrations.RemoveField(
            model_name='item',
            name='updatedat',
        ),
        migrations.RemoveField(
            model_name='item',
            name='updatedby',
        ),
        migrations.AddField(
            model_name='item',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='available',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='item',
            name='defective',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='item',
            name='quantity',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
