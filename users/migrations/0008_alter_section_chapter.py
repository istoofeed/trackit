# Generated by Django 4.2.5 on 2023-12-10 06:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0007_remove_chapter_sections_section_chapter"),
    ]

    operations = [
        migrations.AlterField(
            model_name="section",
            name="chapter",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sections",
                to="users.chapter",
            ),
        ),
    ]