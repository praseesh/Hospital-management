# Generated by Django 5.0.6 on 2024-07-03 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0005_doctoravailability_is_available_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctoravailability',
            name='timeslot',
            field=models.CharField(max_length=40),
        ),
    ]
