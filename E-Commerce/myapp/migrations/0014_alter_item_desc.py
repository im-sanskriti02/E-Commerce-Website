# Generated by Django 3.2.3 on 2021-05-24 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_auto_20210416_0039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='desc',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
