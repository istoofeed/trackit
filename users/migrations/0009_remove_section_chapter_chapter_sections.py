# Generated by Django 4.2.5 on 2023-12-10 06:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0008_alter_section_chapter"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="section",
            name="chapter",
        ),
        migrations.AddField(
            model_name="chapter",
            name="sections",
            field=models.ManyToManyField(to="users.section"),
        ),
    ]
