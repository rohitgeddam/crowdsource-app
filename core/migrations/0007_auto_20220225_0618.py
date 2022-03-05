# Generated by Django 3.1.3 on 2022-02-25 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20220224_1846'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='drop_lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='drop_lng',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='pickup_lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='pickup_lng',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='status',
            field=models.CharField(choices=[('creating', 'Creating'), ('pickup', 'Pickup'), ('droping', 'Droping'), ('payment', 'Payment'), ('complete', 'Complete'), ('canceled', 'Canceled')], default='creating', max_length=20),
        ),
    ]
