# -*- coding: utf-8 -*-
# Generated by Django 1.11b1 on 2017-05-04 11:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FHLBuilder', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commonfile',
            name='fileKind',
            field=models.CharField(choices=[('MV', 'Movie'), ('MC', 'Movie-Cartoon'), ('MM', 'Mini-movie'), ('CC', 'Concert'), ('DD', 'Documentary'), ('TV', 'TV-show'), ('TC', 'TV-Cartoon'), ('TS', 'TV-Sitcom'), ('MS', 'Mini-series'), ('SG', 'song'), ('PT', 'picture'), ('AB', 'audio-book'), ('EB', 'e-book'), ('GG', 'Game'), ('BR', 'BF-random'), ('UN', 'unknown')], default='UN', max_length=10),
        ),
        migrations.AlterField(
            model_name='musician',
            name='albums',
            field=models.ManyToManyField(blank=True, related_name='album_musicians', to='FHLBuilder.Collection'),
        ),
    ]