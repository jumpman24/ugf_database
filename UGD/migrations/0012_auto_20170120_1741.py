# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-20 15:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UGD', '0011_auto_20170118_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pairing',
            name='color',
            field=models.BooleanField(default=True, verbose_name='колір'),
        ),
    ]