# Generated by Django 3.1.3 on 2022-02-24 13:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_category_job'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
