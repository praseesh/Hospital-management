# Generated by Django 5.0.6 on 2024-07-04 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0010_alter_appointment_timeslot_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='is_discharged',
            field=models.BooleanField(default=False),
        ),
    ]
