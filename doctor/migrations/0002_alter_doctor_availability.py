# Generated by Django 5.0.6 on 2024-07-04 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='availability',
            field=models.CharField(blank=True, default='Available', max_length=255, null=True),
        ),
    ]
