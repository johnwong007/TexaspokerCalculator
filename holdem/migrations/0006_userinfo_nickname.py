# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-02 14:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('holdem', '0005_auto_20180202_1121'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='nickname',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='\u6635\u79f0'),
        ),
    ]