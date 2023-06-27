# Generated by Django 4.2.2 on 2023-06-27 08:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0002_wallet"),
    ]

    operations = [
        migrations.CreateModel(
            name="WalletAttribut",
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
                ("address_qr", models.TextField(blank=True, null=True)),
                ("symbol", models.CharField(blank=True, max_length=5, null=True)),
                ("logo", models.TextField(blank=True, null=True)),
                (
                    "wallet",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attributs",
                        to="account.wallet",
                    ),
                ),
            ],
            options={
                "db_table": "account_wallet_attributs",
            },
        ),
    ]
