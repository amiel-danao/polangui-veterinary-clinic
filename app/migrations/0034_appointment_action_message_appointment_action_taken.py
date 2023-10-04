# Generated by Django 4.0.4 on 2023-09-30 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0033_item_picture_alter_appointment_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='action_message',
            field=models.CharField(blank=True, default='', max_length=256),
        ),
        migrations.AddField(
            model_name='appointment',
            name='action_taken',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Pending'), (1, 'Accept'), (2, 'Delete'), (3, 'Decline')], default=0),
        ),
    ]