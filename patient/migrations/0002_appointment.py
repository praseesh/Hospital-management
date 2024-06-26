# Generated by Django 5.0.6 on 2024-06-26 15:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0001_initial'),
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('appointment_id', models.AutoField(primary_key=True, serialize=False)),
                ('appointment_date', models.DateTimeField()),
                ('status', models.CharField(choices=[('scheduled', 'Scheduled'), ('completed', 'Completed'), ('canceled', 'Canceled')], default='scheduled', max_length=50)),
                ('reason_for_visit', models.TextField(choices=[('fever', 'Fever'), ('headache', 'Headache'), ('flu', 'Flu'), ('covid', 'COVID-19'), ('diabetes', 'Diabetes'), ('hypertension', 'Hypertension'), ('asthma', 'Asthma'), ('arthritis', 'Arthritis'), ('cancer', 'Cancer'), ('depression', 'Depression'), ('allergy', 'Allergy'), ('pneumonia', 'Pneumonia'), ('bronchitis', 'Bronchitis'), ('migraine', 'Migraine'), ('insomnia', 'Insomnia'), ('other', 'Other')], default='Other')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.patient')),
            ],
            options={
                'db_table': 'appointment',
            },
        ),
    ]