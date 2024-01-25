# Generated by Django 4.2.5 on 2024-01-18 03:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0010_remove_chapter_sections_section_chapter"),
    ]

    operations = [
        migrations.AddField(
            model_name="group",
            name="is_approved",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="user",
            name="in_group",
            field=models.BooleanField(default=False),
        ),
    ]