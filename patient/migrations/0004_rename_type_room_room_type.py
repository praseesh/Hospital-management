# Generated by Django 5.0.6 on 2024-06-24 07:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0003_room_alter_patient_admission_date_patient_room'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='type',
            new_name='room_type',
        ),
    ]