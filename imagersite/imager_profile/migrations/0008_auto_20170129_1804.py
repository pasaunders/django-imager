# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-30 02:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imager_profile', '0007_auto_20170124_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagerprofile',
            name='address',
            field=models.CharField(blank=True, default='', max_length=70, null=True),
        ),
        migrations.AlterField(
            model_name='imagerprofile',
            name='camera_type',
            field=models.CharField(blank=True, choices=[('Nikon', 'Nikon'), ('iPhone', 'iPhone'), ('Canon', 'Canon'), ('--------', '--------')], default='--------', max_length=10),
        ),
        migrations.AlterField(
            model_name='imagerprofile',
            name='phone_number',
            field=models.CharField(blank=True, default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='imagerprofile',
            name='photography_type',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='imagerprofile',
            name='travel_distance',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]