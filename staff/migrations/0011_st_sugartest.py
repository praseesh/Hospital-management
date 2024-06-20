# Generated by Django 5.0.6 on 2024-06-19 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0010_remove_prescription_date_issued_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ST',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('investigation', models.CharField(max_length=50)),
                ('reference_value', models.CharField(max_length=20)),
                ('unit', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'st',
            },
        ),
        migrations.CreateModel(
            name='SugarTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('investigation', models.CharField(default='Fasting Blood Sugar, Postprandial Blood Sugar, Random Blood Sugar, HbA1c, Oral Glucose Tolerance Test (OGTT)', max_length=50)),
                ('result', models.CharField(max_length=255)),
                ('reference_value', models.CharField(default='70 - 100, 70 - 140, 70 - 140, 4.0 - 5.6, 140 - 199', max_length=20)),
                ('unit', models.CharField(default='mg/dL, mg/dL, mg/dL, %, mg/dL', max_length=10)),
            ],
            options={
                'db_table': 'sugar_test',
            },
        ),
    ]