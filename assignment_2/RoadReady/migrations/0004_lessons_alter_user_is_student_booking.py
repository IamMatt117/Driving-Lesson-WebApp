# Generated by Django 4.2.6 on 2023-11-15 21:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RoadReady', '0003_user_is_instructor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lessons',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('lesson_type', models.CharField(default=True, max_length=10)),
                ('duration', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='is_student',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(null=True)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField(null=True)),
                ('lessons', models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='RoadReady.lessons')),
                ('user_id', models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
