# Generated by Django 4.2.6 on 2023-11-15 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RoadReady', '0002_user_is_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_instructor',
            field=models.BooleanField(default=False),
        ),
    ]
