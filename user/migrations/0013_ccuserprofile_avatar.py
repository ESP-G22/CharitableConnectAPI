# Generated by Django 4.1 on 2023-03-15 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0012_remove_ccuserprofile_avatar"),
    ]

    operations = [
        migrations.AddField(
            model_name="ccuserprofile",
            name="avatar",
            field=models.UUIDField(blank=True, null=True),
        ),
    ]
