# Generated by Django 4.2.16 on 2024-11-06 14:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('coach', '0016_rename_date_logged_loggedworkout_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='loggedworkout',
            name='assigned_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
