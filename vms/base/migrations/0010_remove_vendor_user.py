# Generated by Django 5.0.4 on 2024-05-07 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_vendor_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='user',
        ),
    ]
