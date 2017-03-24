# -*- coding: utf-8 -*-
# Generated by Django 1.11b1 on 2017-03-24 22:34
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
                ('slug', models.SlugField(max_length=31, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filepath', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=31, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Common',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileKind', models.CharField(choices=[('A', 'Audio'), ('V', 'Video')], default='A', max_length=1)),
                ('filename', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=31, unique=True)),
                ('slug', models.SlugField(max_length=31, unique=True)),
                ('year', models.IntegerField(default=0)),
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
                ('name', models.CharField(max_length=31, unique=True)),
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
                ('name', models.CharField(max_length=31, unique=True)),
                ('slug', models.SlugField(max_length=31, unique=True)),
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
            name='Album',
            fields=[
                ('collection_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='FHLBuilder.Collection')),
            ],
            bases=('FHLBuilder.collection',),
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
                ('common_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='FHLBuilder.Common')),
            ],
            bases=('FHLBuilder.common',),
        ),
        migrations.CreateModel(
            name='Musician',
            fields=[
                ('artist_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='FHLBuilder.Artist')),
                ('albums', models.ManyToManyField(blank=True, to='FHLBuilder.Album')),
                ('concerts', models.ManyToManyField(blank=True, to='FHLBuilder.Movie')),
            ],
            bases=('FHLBuilder.artist',),
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('collection_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='FHLBuilder.Collection')),
                ('episodes', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='FHLBuilder.Movie')),
            ],
            bases=('FHLBuilder.collection',),
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('common_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='FHLBuilder.Common')),
                ('track', models.IntegerField()),
            ],
            bases=('FHLBuilder.common',),
        ),
        migrations.AddField(
            model_name='common',
            name='tag',
            field=models.ManyToManyField(blank=True, to='FHLBuilder.Tag'),
        ),
        migrations.AddField(
            model_name='collection',
            name='members',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='FHLBuilder.Common'),
        ),
        migrations.AddField(
            model_name='director',
            name='movies',
            field=models.ManyToManyField(blank=True, to='FHLBuilder.Movie'),
        ),
        migrations.AddField(
            model_name='album',
            name='songs',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='FHLBuilder.Song'),
        ),
        migrations.AddField(
            model_name='actor',
            name='movies',
            field=models.ManyToManyField(blank=True, to='FHLBuilder.Movie'),
        ),
    ]
