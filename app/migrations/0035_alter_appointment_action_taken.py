# Generated by Django 4.0.4 on 2023-09-30 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0034_appointment_action_message_appointment_action_taken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='action_taken',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Accept'), (2, 'Delete'), (3, 'Decline')], default=1),
        ),
    ]