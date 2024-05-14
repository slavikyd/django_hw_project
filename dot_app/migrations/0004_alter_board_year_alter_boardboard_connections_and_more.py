# Generated by Django 5.0.3 on 2024-05-06 11:20

import datetime
import django.db.models.deletion
import dot_app.models
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dot_app", "0003_boardboard_connections_alter_board_created_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="board",
            name="year",
            field=models.IntegerField(
                blank=True, null=True, validators=[dot_app.models.check_year]
            ),
        ),
        migrations.AlterField(
            model_name="boardboard",
            name="connections",
            field=models.TextField(
                choices=[
                    ("USB/UART", "USB with UART support"),
                    ("USB/COM", "USB with COM support"),
                    ("USB", "plain USB"),
                    ("USB-C:USB-A", "USB-C to USB-A connection"),
                    ("USB-Micro:USB-A", "Micro USB to USB-A connection"),
                ],
                default="USB/COM",
            ),
        ),
        migrations.CreateModel(
            name="BoardClient",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        blank=True,
                        default=datetime.datetime.now,
                        null=True,
                        validators=[dot_app.models.check_created],
                    ),
                ),
                (
                    "board",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dot_app.board",
                        verbose_name="board",
                    ),
                ),
            ],
            options={
                "verbose_name": "relationship board client",
                "verbose_name_plural": "relationships boards client",
                "db_table": '"databank"."board_client"',
            },
        ),
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        blank=True,
                        default=datetime.datetime.now,
                        null=True,
                        validators=[dot_app.models.check_created],
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        blank=True,
                        default=datetime.datetime.now,
                        null=True,
                        validators=[dot_app.models.check_modified],
                    ),
                ),
                (
                    "boards",
                    models.ManyToManyField(
                        through="dot_app.BoardClient",
                        to="dot_app.board",
                        verbose_name="boards",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "client",
                "verbose_name_plural": "clients",
                "db_table": '"databank"."client"',
            },
        ),
        migrations.AddField(
            model_name="boardclient",
            name="client",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="dot_app.client",
                verbose_name="client",
            ),
        ),
    ]