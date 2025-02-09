# Generated by Django 4.2.5 on 2023-11-19 21:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RoadReady', '0018_remove_product_instructor_product_instructors'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(max_length=16)),
                ('card_holder', models.CharField(max_length=200)),
                ('expiry_date', models.DateField()),
                ('cvv', models.CharField(max_length=3)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RoadReady.product')),
            ],
        ),
    ]
