# Generated by Django 4.2.5 on 2023-12-10 05:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0005_chapter_chapter_progress_chapter_total_section"),
    ]

    operations = [
        migrations.AlterField(
            model_name="section",
            name="date_finished",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]