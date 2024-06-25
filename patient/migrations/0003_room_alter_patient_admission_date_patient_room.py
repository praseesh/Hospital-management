# Generated by Django 5.0.6 on 2024-06-23 06:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0002_alter_patient_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.CharField(max_length=50, unique=True)),
                ('type', models.CharField(choices=[('General', 'General'), ('ICU', 'ICU'), ('Rooms', 'Rooms')], max_length=50)),
                ('is_vacant', models.BooleanField(default=True)),
                ('price', models.IntegerField()),
            ],
            options={
                'db_table': 'rooms',
            },
        ),
        migrations.AlterField(
            model_name='patient',
            name='admission_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='patient.room'),
        ),
    ]