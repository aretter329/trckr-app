# Generated by Django 4.2.16 on 2024-10-01 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coach', '0003_day_rename_body_program_notes_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exercise',
            name='reps',
        ),
        migrations.RemoveField(
            model_name='exercise',
            name='sets',
        ),
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reps', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coach.exercise')),
            ],
        ),
    ]
