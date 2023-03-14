# Generated by Django 4.1 on 2023-03-14 19:23

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        auto_created=True,
                        default=uuid.UUID("85cd2acf-a6fa-47e1-a69b-803b32141c87"),
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("file", models.ImageField(upload_to="images/")),
            ],
        ),
    ]