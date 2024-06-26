# Generated by Django 5.0.4 on 2024-04-30 20:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_vendor_average_response_time_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalPerformance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('on_time_delivery_rate', models.FloatField(default=0)),
                ('quality_rating_avg', models.FloatField(default=0)),
                ('average_response_time', models.FloatField(default=0)),
                ('fullfilment_rate', models.FloatField(default=0)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='performances', to='base.vendor')),
            ],
        ),
    ]
