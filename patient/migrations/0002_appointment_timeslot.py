# Generated by Django 5.0.6 on 2024-07-02 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='timeslot',
            field=models.IntegerField(choices=[(0, '09:00 - 09:30'), (1, '10:00 - 10:30'), (2, '11:00 - 11:30'), (3, '12:00 - 12:30'), (4, '13:00 - 13:30'), (5, '14:00 - 14:30'), (6, '15:00 - 15:30'), (7, '16:00 - 16:30'), (8, '17:00 - 17:30')], default=0),
        ),
    ]