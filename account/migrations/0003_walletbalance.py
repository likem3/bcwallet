# Generated by Django 4.2.2 on 2023-07-06 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0002_walletattribut"),
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
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, help_text="creation datetime"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, help_text="updated datetime"),
                ),
                (
                    "amount",
                    models.DecimalField(
                        blank=True,
                        decimal_places=10,
                        help_text="Nominal amount in the wallet",
                        max_digits=25,
                        null=True,
                    ),
                ),
                (
                    "amount_change",
                    models.DecimalField(
                        blank=True,
                        decimal_places=10,
                        help_text="Nominal amount in the wallet",
                        max_digits=25,
                        null=True,
                    ),
                ),
                (
                    "unit",
                    models.CharField(
                        blank=True,
                        help_text="Symbol of the wallet currency",
                        max_length=10,
                        null=True,
                    ),
                ),
                (
                    "wallet",
                    models.ForeignKey(
                        blank=True,
                        help_text="Related wallet object",
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
