# Generated by Django 5.0.6 on 2024-06-26 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0003_remove_invoice_labreport_bill_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='status',
            field=models.CharField(default='pending', max_length=50),
        ),
    ]