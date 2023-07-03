# Generated by Django 4.2.2 on 2023-06-29 09:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recharge", "0003_transaction_blockchain"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("confirming", "Confirming"),
                    ("completed", "Completed"),
                    ("failed", "Failed"),
                    ("cancelled", "Cancelled"),
                ],
                default="pending",
                max_length=20,
            ),
        ),
    ]
