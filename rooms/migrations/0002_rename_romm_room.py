# Generated by Django 4.1.2 on 2022-10-20 19:18

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Romm',
            new_name='Room',
        ),
    ]
