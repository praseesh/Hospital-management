# Generated by Django 5.0.6 on 2024-07-03 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0004_alter_doctoravailability_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctoravailability',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('scheduled', 'Scheduled'), ('canceled', 'Canceled')], default='scheduled', max_length=50),
        ),
    ]
