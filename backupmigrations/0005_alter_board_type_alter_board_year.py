# Generated by Django 5.0.3 on 2024-05-14 19:00

import dot_app.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dot_app", "0004_alter_board_year_alter_boardboard_connections_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="board",
            name="type",
            field=models.TextField(blank=True, default="Undefined", null=True),
        ),
        migrations.AlterField(
            model_name="board",
            name="year",
            field=models.IntegerField(
                blank=True,
                default=2024,
                null=True,
                validators=[dot_app.models.check_year],
            ),
        ),
    ]
