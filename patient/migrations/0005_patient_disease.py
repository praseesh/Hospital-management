# Generated by Django 5.0.6 on 2024-06-24 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0004_rename_type_room_room_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='disease',
            field=models.CharField(choices=[('fever', 'Fever'), ('headache', 'Headache'), ('flu', 'Flu'), ('covid', 'COVID-19'), ('diabetes', 'Diabetes'), ('hypertension', 'Hypertension'), ('asthma', 'Asthma'), ('arthritis', 'Arthritis'), ('cancer', 'Cancer'), ('depression', 'Depression'), ('allergy', 'Allergy'), ('pneumonia', 'Pneumonia'), ('bronchitis', 'Bronchitis'), ('migraine', 'Migraine'), ('insomnia', 'Insomnia'), ('other', 'Other')], default='', max_length=50),
        ),
    ]