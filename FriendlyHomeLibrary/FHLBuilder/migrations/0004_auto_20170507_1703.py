# -*- coding: utf-8 -*-
# Generated by Django 1.11b1 on 2017-05-07 17:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FHLBuilder', '0003_commonfile_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='collection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='songs', to='FHLBuilder.Collection'),
        ),
    ]