# Generated by Django 5.0.6 on 2024-06-26 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0002_appointment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='appointment_id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]
