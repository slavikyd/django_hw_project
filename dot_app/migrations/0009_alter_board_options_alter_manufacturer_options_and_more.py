# Generated by Django 4.2.13 on 2024-05-26 17:48

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("dot_app", "0008_board_datasheet_board_image"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="board",
            options={"ordering": ["-id"]},
        ),
        migrations.AlterModelOptions(
            name="manufacturer",
            options={"ordering": ["-id"]},
        ),
        migrations.AlterModelOptions(
            name="subtype",
            options={"ordering": ["-id"]},
        ),
    ]