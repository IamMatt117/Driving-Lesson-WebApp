# Generated by Django 4.2.6 on 2023-11-16 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RoadReady', '0008_alter_instructor_profile_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructor',
            name='first_name',
            field=models.TextField(max_length=15),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='last_name',
            field=models.TextField(max_length=15),
        ),
    ]
