# Generated by Django 4.2.6 on 2023-11-18 17:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RoadReady', '0010_feedback'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='satisfy',
        ),
    ]
