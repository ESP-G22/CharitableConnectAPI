# Generated by Django 4.1 on 2023-02-27 00:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="address",
            old_name="building_name",
            new_name="buildingName",
        ),
        migrations.RenameField(
            model_name="address",
            old_name="street_name",
            new_name="streetName",
        ),
        migrations.RenameField(
            model_name="address",
            old_name="town_city",
            new_name="townCity",
        ),
        migrations.RemoveField(
            model_name="event",
            name="attendee_count",
        ),
        migrations.RemoveField(
            model_name="event",
            name="pub_date",
        ),
        migrations.AddField(
            model_name="address",
            name="lat",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="address",
            name="lon",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="event",
            name="address",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="events.address",
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="pubDate",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="date published",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="event",
            name="organiser",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
