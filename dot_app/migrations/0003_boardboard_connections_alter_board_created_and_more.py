# Generated by Django 5.0.3 on 2024-04-30 06:44

import datetime
import dot_app.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dot_app", "0002_boardboard"),
    ]

    operations = [
        migrations.AddField(
            model_name="boardboard",
            name="connections",
            field=models.TextField(default="USB/UART"),
        ),
        migrations.AlterField(
            model_name="board",
            name="created",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime.now,
                null=True,
                validators=[dot_app.models.check_created],
            ),
        ),
        migrations.AlterField(
            model_name="board",
            name="modified",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime.now,
                null=True,
                validators=[dot_app.models.check_modified],
            ),
        ),
        migrations.AlterField(
            model_name="boardboard",
            name="created",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime.now,
                null=True,
                validators=[dot_app.models.check_created],
            ),
        ),
        migrations.AlterField(
            model_name="boardmanufacturer",
            name="created",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime.now,
                null=True,
                validators=[dot_app.models.check_created],
            ),
        ),
        migrations.AlterField(
            model_name="boardsubtype",
            name="created",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime.now,
                null=True,
                validators=[dot_app.models.check_created],
            ),
        ),
        migrations.AlterField(
            model_name="manufacturer",
            name="created",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime.now,
                null=True,
                validators=[dot_app.models.check_created],
            ),
        ),
        migrations.AlterField(
            model_name="manufacturer",
            name="modified",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime.now,
                null=True,
                validators=[dot_app.models.check_modified],
            ),
        ),
        migrations.AlterField(
            model_name="subtype",
            name="created",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime.now,
                null=True,
                validators=[dot_app.models.check_created],
            ),
        ),
        migrations.AlterField(
            model_name="subtype",
            name="modified",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime.now,
                null=True,
                validators=[dot_app.models.check_modified],
            ),
        ),
    ]
