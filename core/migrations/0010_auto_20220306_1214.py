# Generated by Django 3.1.3 on 2022-03-06 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20220306_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='distance',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='job',
            name='pricing',
            field=models.IntegerField(default=0),
        ),
    ]