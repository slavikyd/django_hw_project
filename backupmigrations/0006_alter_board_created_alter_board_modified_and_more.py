# Generated by Django 5.0.3 on 2024-05-15 06:17

import datetime
import dot_app.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dot_app", "0005_alter_board_type_alter_board_year"),
    ]

    operations = [
        migrations.AlterField(
            model_name="board",
            name="created",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(
                    2024, 5, 15, 6, 17, 46, 862843, tzinfo=datetime.timezone.utc
                ),
                null=True,
                validators=[dot_app.models.check_created],
            ),
        ),
        migrations.AlterField(
            model_name="board",
            name="modified",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(
                    2024, 5, 15, 6, 17, 46, 862843, tzinfo=datetime.timezone.utc
                ),
                null=True,
                validators=[dot_app.models.check_modified],
            ),
        ),
        migrations.AlterField(
            model_name="boardboard",
            name="created",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(
                    2024, 5, 15, 6, 17, 46, 862843, tzinfo=datetime.timezone.utc
                ),
                null=True,
                validators=[dot_app.models.check_created],
            ),
        ),
        migrations.AlterField(
            model_name="boardclient",
            name="created",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(
                    2024, 5, 15, 6, 17, 46, 862843, tzinfo=datetime.timezone.utc
                ),
                null=True,
                validators=[dot_app.models.check_created],
            ),
        ),
        migrations.AlterField(
            model_name="boardmanufacturer",
            name="created",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(
                    2024, 5, 15, 6, 17, 46, 862843, tzinfo=datetime.timezone.utc
                ),
                null=True,
                validators=[dot_app.models.check_created],
            ),
        ),
        migrations.AlterField(
            model_name="boardsubtype",
            name="created",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(
                    2024, 5, 15, 6, 17, 46, 862843, tzinfo=datetime.timezone.utc
                ),
                null=True,
                validators=[dot_app.models.check_created],
            ),
        ),
        migrations.AlterField(
            model_name="client",
            name="created",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(
                    2024, 5, 15, 6, 17, 46, 862843, tzinfo=datetime.timezone.utc
                ),
                null=True,
                validators=[dot_app.models.check_created],
            ),
        ),
        migrations.AlterField(
            model_name="client",
            name="modified",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(
                    2024, 5, 15, 6, 17, 46, 862843, tzinfo=datetime.timezone.utc
                ),
                null=True,
                validators=[dot_app.models.check_modified],
            ),
        ),
        migrations.AlterField(
            model_name="manufacturer",
            name="created",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(
                    2024, 5, 15, 6, 17, 46, 862843, tzinfo=datetime.timezone.utc
                ),
                null=True,
                validators=[dot_app.models.check_created],
            ),
        ),
        migrations.AlterField(
            model_name="manufacturer",
            name="modified",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(
                    2024, 5, 15, 6, 17, 46, 862843, tzinfo=datetime.timezone.utc
                ),
                null=True,
                validators=[dot_app.models.check_modified],
            ),
        ),
        migrations.AlterField(
            model_name="subtype",
            name="created",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(
                    2024, 5, 15, 6, 17, 46, 862843, tzinfo=datetime.timezone.utc
                ),
                null=True,
                validators=[dot_app.models.check_created],
            ),
        ),
        migrations.AlterField(
            model_name="subtype",
            name="modified",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(
                    2024, 5, 15, 6, 17, 46, 862843, tzinfo=datetime.timezone.utc
                ),
                null=True,
                validators=[dot_app.models.check_modified],
            ),
        ),
    ]
