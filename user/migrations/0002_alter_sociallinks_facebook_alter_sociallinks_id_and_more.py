# Generated by Django 4.1 on 2023-02-25 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sociallinks",
            name="facebook",
            field=models.URLField(default=""),
        ),
        migrations.AlterField(
            model_name="sociallinks",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="sociallinks",
            name="instagram",
            field=models.URLField(default=""),
        ),
        migrations.AlterField(
            model_name="sociallinks",
            name="twitter",
            field=models.URLField(default=""),
        ),
        migrations.AlterField(
            model_name="sociallinks",
            name="website",
            field=models.URLField(default=""),
        ),
    ]
