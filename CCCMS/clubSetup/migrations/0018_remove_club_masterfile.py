# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-17 23:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubSetup', '0017_club_masterfile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='club',
            name='masterFile',
        ),
    ]
