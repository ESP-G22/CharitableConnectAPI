# Generated by Django 4.1.7 on 2023-04-23 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_alter_event_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='type',
            field=models.CharField(choices=[('LocalBusiness', 'Local Business'), ('Climate', 'Climate'), ('Community', 'Community'), ('Sports', 'Sports'), ('Other', 'Other')], default='Other', max_length=20),
        ),
    ]
