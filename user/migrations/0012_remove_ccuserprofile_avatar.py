# Generated by Django 4.1 on 2023-03-15 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0011_alter_ccuserprofile_avatar"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ccuserprofile",
            name="avatar",
        ),
    ]
