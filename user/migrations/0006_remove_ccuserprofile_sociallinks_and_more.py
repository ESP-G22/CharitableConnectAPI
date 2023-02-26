# Generated by Django 4.1 on 2023-02-26 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0005_remove_ccuser_bio_remove_ccuser_followedusers_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ccuserprofile",
            name="socialLinks",
        ),
        migrations.AddField(
            model_name="ccuserprofile",
            name="facebook",
            field=models.URLField(default=""),
        ),
        migrations.AddField(
            model_name="ccuserprofile",
            name="instagram",
            field=models.URLField(default=""),
        ),
        migrations.AddField(
            model_name="ccuserprofile",
            name="twitter",
            field=models.URLField(default=""),
        ),
        migrations.AddField(
            model_name="ccuserprofile",
            name="website",
            field=models.URLField(default=""),
        ),
        migrations.DeleteModel(
            name="SocialLinks",
        ),
    ]
