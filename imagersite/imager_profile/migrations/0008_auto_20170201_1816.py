# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-02 02:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imager_profile', '0007_auto_20170124_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagerprofile',
            name='travel_distance',
            field=models.IntegerField(default=0),
        ),
    ]
