# Generated by Django 4.2.2 on 2023-07-08 11:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0005_alter_wallettask_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="walletbalance",
            name="last_updated_at",
            field=models.DateTimeField(
                blank=True, help_text="last updated datetime", null=True
            ),
        ),
        migrations.AlterField(
            model_name="wallettask",
            name="status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("open", "Open"),
                    ("success", "Success"),
                    ("fail", "Fail"),
                    ("cencel", "Cancel"),
                ],
                default="open",
                help_text="Number of attemp running task",
                max_length=20,
                null=True,
            ),
        ),
    ]