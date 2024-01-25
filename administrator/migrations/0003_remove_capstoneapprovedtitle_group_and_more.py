# Generated by Django 4.2.5 on 2023-12-07 08:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("administrator", "0002_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="capstoneapprovedtitle",
            name="group",
        ),
        migrations.AddField(
            model_name="capstoneapprovedtitle",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="capstoneapprovedtitle",
            name="description",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="capstoneapprovedtitle",
            name="file",
            field=models.FileField(blank=True, upload_to=""),
        ),
        migrations.AddField(
            model_name="capstoneapprovedtitle",
            name="group_members",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
