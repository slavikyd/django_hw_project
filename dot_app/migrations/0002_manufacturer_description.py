# Generated by Django 4.2.13 on 2024-06-14 18:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dot_app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="manufacturer",
            name="description",
            field=models.TextField(default="Nothing to look for here", null=True),
        ),
    ]
