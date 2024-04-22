# Generated by Django 5.0.4 on 2024-04-11 20:16

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_foodbooking_room_id_delete_rooms'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rooms',
            fields=[
                ('room_number', models.BigAutoField(default=101, primary_key=True, serialize=False, unique=True)),
                ('beddings', models.IntegerField(default=1)),
                ('room_type', models.CharField(choices=[('suite', 'Suite'), ('premium', 'Premium'), ('standard', 'Standard'), ('dormitory', 'Dormitory')], max_length=100)),
                ('features', models.CharField(choices=[('free breakfast', 'Free Breakfast'), ('free internet', 'Free Internet'), ('lunch included', 'Lunch Included')], max_length=100)),
                ('room_status', models.CharField(choices=[('available', 'available'), ('unavailable', 'unavailable')], max_length=100)),
                ('adult', models.IntegerField(default=1)),
                ('children', models.IntegerField(default=0)),
                ('check_in', models.DateField(default=datetime.date(2024, 4, 12))),
                ('check_out', models.DateField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.customer')),
            ],
        ),
        migrations.DeleteModel(
            name='FoodBooking',
        ),
    ]