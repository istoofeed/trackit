# Generated by Django 4.2.5 on 2024-01-18 07:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0011_group_is_approved_user_in_group"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="chapter",
            options={"ordering": ["created_at"]},
        ),
        migrations.AddField(
            model_name="chapter",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
