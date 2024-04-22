# Generated by Django 5.0.4 on 2024-04-11 20:18

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rooms_delete_foodbooking'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=1000)),
                ('item_price', models.IntegerField()),
                ('item_quantity', models.IntegerField()),
                ('date', models.DateField(default=datetime.date(2024, 4, 12))),
                ('customer_name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.customer')),
                ('room_details', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.rooms')),
            ],
        ),
    ]