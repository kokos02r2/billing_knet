# Generated by Django 4.1 on 2024-01-20 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tinkoff_payments', '0002_alter_paymenttinkoff_payment_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymenttinkoff',
            name='amount',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
