# Generated by Django 4.2.2 on 2023-06-28 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0003_walletattribut"),
    ]

    operations = [
        migrations.CreateModel(
            name="WalletBalance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "amount",
                    models.DecimalField(
                        blank=True, decimal_places=10, max_digits=25, null=True
                    ),
                ),
                ("unit", models.CharField(blank=True, max_length=10, null=True)),
                ("created_timestamp", models.DateTimeField(blank=True, null=True)),
                (
                    "wallet",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="balance",
                        to="account.wallet",
                    ),
                ),
            ],
            options={
                "db_table": "account_wallet_balance",
            },
        ),
    ]
