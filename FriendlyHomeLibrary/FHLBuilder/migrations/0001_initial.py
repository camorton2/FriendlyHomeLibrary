# -*- coding: utf-8 -*-
# Generated by Django 1.11b1 on 2017-03-25 20:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullName', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filePath', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CommonFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileKind', models.CharField(choices=[('A', 'Audio'), ('V', 'Video')], default='A', max_length=1)),
                ('fileName', models.CharField(max_length=100)),
                ('year', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='FHLUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userMode', models.CharField(choices=[('B', 'Builder'), ('R', 'Reader')], default='R', max_length=1)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Setup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('songsHead', models.CharField(max_length=100)),
                ('moviesHead', models.CharField(max_length=100)),
                ('booksHead', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('artist_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='FHLBuilder.Artist')),
            ],
            bases=('FHLBuilder.artist',),
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('artist_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='FHLBuilder.Artist')),
            ],
            bases=('FHLBuilder.artist',),
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('commonfile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='FHLBuilder.CommonFile')),
            ],
            bases=('FHLBuilder.commonfile',),
        ),
        migrations.CreateModel(
            name='Musician',
            fields=[
                ('artist_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='FHLBuilder.Artist')),
                ('albums', models.ManyToManyField(blank=True, to='FHLBuilder.Collection')),
                ('concerts', models.ManyToManyField(blank=True, to='FHLBuilder.Movie')),
            ],
            bases=('FHLBuilder.artist',),
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('commonfile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='FHLBuilder.CommonFile')),
                ('track', models.IntegerField()),
            ],
            bases=('FHLBuilder.commonfile',),
        ),
        migrations.AddField(
            model_name='commonfile',
            name='collection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='FHLBuilder.Collection'),
        ),
        migrations.AddField(
            model_name='commonfile',
            name='tags',
            field=models.ManyToManyField(blank=True, to='FHLBuilder.Tag'),
        ),
        migrations.AddField(
            model_name='musician',
            name='songs',
            field=models.ManyToManyField(blank=True, to='FHLBuilder.Song'),
        ),
        migrations.AddField(
            model_name='director',
            name='movies',
            field=models.ManyToManyField(blank=True, to='FHLBuilder.Movie'),
        ),
        migrations.AddField(
            model_name='actor',
            name='movies',
            field=models.ManyToManyField(blank=True, to='FHLBuilder.Movie'),
        ),
    ]