# Generated by Django 5.0.4 on 2024-04-18 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_remove_rooms_adult_remove_rooms_check_in_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rooms',
            name='room_image',
            field=models.ImageField(blank=True, upload_to='hotel images/'),
        ),
    ]
