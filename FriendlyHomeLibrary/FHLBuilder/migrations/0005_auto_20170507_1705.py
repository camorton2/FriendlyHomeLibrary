# -*- coding: utf-8 -*-
# Generated by Django 1.11b1 on 2017-05-07 17:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FHLBuilder', '0004_auto_20170507_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='collection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='books', to='FHLBuilder.Collection'),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='collection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chapters', to='FHLBuilder.Collection'),
        ),
        migrations.AlterField(
            model_name='game',
            name='collection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='games', to='FHLBuilder.Collection'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='collection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='movies', to='FHLBuilder.Collection'),
        ),
        migrations.AlterField(
            model_name='picture',
            name='collection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pictures', to='FHLBuilder.Collection'),
        ),
    ]