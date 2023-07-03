# Generated by Django 4.2.2 on 2023-06-28 11:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recharge", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="transaction",
            name="amount",
            field=models.DecimalField(
                blank=True, decimal_places=10, max_digits=25, null=True
            ),
        ),
    ]
