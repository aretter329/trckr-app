# Generated by Django 4.2.16 on 2024-10-01 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coach', '0004_remove_exercise_reps_remove_exercise_sets_set'),
    ]

    operations = [
        migrations.AddField(
            model_name='set',
            name='number',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
