# Generated by Django 4.2.2 on 2023-07-25 11:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("merchant", "0001_initial"),
        ("recharge", "0006_alter_transaction_transaction_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="merchant",
            field=models.ForeignKey(
                blank=True,
                default=None,
                help_text="merchant of the system",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="merchant_transactions",
                to="merchant.merchant",
            ),
        ),
    ]
