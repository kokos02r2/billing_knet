# Generated by Django 4.1 on 2024-01-20 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tinkoff_payments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymenttinkoff',
            name='payment_id',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
