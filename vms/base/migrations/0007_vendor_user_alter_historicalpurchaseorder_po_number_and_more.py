# Generated by Django 5.0.4 on 2024-05-06 15:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_historicalpurchaseorder'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='historicalpurchaseorder',
            name='po_number',
            field=models.CharField(blank=True, db_index=True, max_length=18),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='po_number',
            field=models.CharField(blank=True, max_length=18, unique=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='vendor_code',
            field=models.CharField(blank=True, max_length=18, unique=True),
        ),
    ]
