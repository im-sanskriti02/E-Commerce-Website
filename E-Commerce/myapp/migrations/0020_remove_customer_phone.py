# Generated by Django 3.2.3 on 2021-06-16 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0019_auto_20210616_2348'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='phone',
        ),
    ]