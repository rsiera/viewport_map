# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-21 20:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='locationpoint',
            unique_together=set([('address', 'longitude', 'latitude')]),
        ),
    ]
