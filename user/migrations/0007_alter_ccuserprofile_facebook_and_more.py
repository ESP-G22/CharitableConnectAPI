# Generated by Django 4.1 on 2023-02-26 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0006_remove_ccuserprofile_sociallinks_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ccuserprofile",
            name="facebook",
            field=models.URLField(default="", null=True),
        ),
        migrations.AlterField(
            model_name="ccuserprofile",
            name="instagram",
            field=models.URLField(default="", null=True),
        ),
        migrations.AlterField(
            model_name="ccuserprofile",
            name="twitter",
            field=models.URLField(default="", null=True),
        ),
        migrations.AlterField(
            model_name="ccuserprofile",
            name="website",
            field=models.URLField(default="", null=True),
        ),
    ]