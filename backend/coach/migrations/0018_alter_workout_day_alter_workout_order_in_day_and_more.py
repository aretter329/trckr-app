# Generated by Django 4.2.16 on 2024-11-20 16:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coach', '0017_loggedworkout_assigned_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workout',
            name='day',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='workouts', to='coach.day'),
        ),
        migrations.AlterField(
            model_name='workout',
            name='order_in_day',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='WorkoutGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('athletes', models.ManyToManyField(blank=True, related_name='athlete_workout_groups', to=settings.AUTH_USER_MODEL)),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coached_workout_groups', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
