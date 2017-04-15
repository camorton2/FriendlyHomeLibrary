# -*- coding: utf-8 -*-
# Generated by Django 1.11b1 on 2017-04-15 17:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullName', models.CharField(max_length=1000)),
                ('slug', models.SlugField(max_length=1000, unique=True)),
            ],
            options={
                'ordering': ['fullName'],
                'permissions': (('artist_builder', 'artist builder'), ('artist_reader', 'artist reader')),
            },
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filePath', models.CharField(max_length=1000)),
                ('drive', models.IntegerField()),
                ('title', models.CharField(max_length=1000)),
                ('slug', models.SlugField(max_length=1000, unique=True)),
            ],
            options={
                'ordering': ['title'],
                'permissions': (('collection_builder', 'collection builder'), ('collection_reader', 'collection reader')),
            },
        ),
        migrations.CreateModel(
            name='CommonFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileKind', models.CharField(choices=[(b'UN', b'unknown'), (b'MV', b'Movie'), (b'MM', b'Mini-movie'), (b'CC', b'Concert'), (b'DD', b'Documentary'), (b'TV', b'TV-show'), (b'MS', b'Mini-series'), (b'AB', b'audio-book'), (b'EB', b'e-book'), (b'SG', b'song'), (b'PT', b'picture'), (b'GG', b'Game')], default=b'UN', max_length=10)),
                ('fileName', models.CharField(max_length=1000)),
                ('year', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=1000)),
                ('slug', models.SlugField(max_length=1000, unique=True)),
            ],
            options={
                'ordering': ['title'],
                'permissions': (('common_builder', 'common builder'), ('common_reader', 'common reader')),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000, unique=True)),
                ('slug', models.SlugField(max_length=1000, unique=True)),
            ],
            options={
                'ordering': ['name'],
                'permissions': (('tag_builder', 'tag builder'), ('tag_reader', 'tag reader')),
            },
        ),
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('artist_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='FHLBuilder.Artist')),
            ],
            options={
                'permissions': (('actor_builder', 'actor builder'), ('actor_reader', 'actor reader')),
            },
            bases=('FHLBuilder.artist',),
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('commonfile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='FHLBuilder.CommonFile')),
                ('collection', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='FHLBuilder.Collection')),
                ('dislikes', models.ManyToManyField(blank=True, related_name='book_dislikes', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(blank=True, related_name='book_likes', to=settings.AUTH_USER_MODEL)),
                ('loves', models.ManyToManyField(blank=True, related_name='book_loves', to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(blank=True, related_name='book_tags', to='FHLBuilder.Tag')),
            ],
            options={
                'permissions': (('book_builder', 'book builder'), ('book_reader', 'book reader')),
            },
            bases=('FHLBuilder.commonfile',),
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('commonfile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='FHLBuilder.CommonFile')),
                ('collection', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='FHLBuilder.Collection')),
            ],
            options={
                'permissions': (('chapter_builder', 'chapter builder'), ('chapter_reader', 'chapter reader')),
            },
            bases=('FHLBuilder.commonfile',),
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('artist_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='FHLBuilder.Artist')),
            ],
            options={
                'permissions': (('director_builder', 'director builder'), ('director_reader', 'director reader')),
            },
            bases=('FHLBuilder.artist',),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('commonfile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='FHLBuilder.CommonFile')),
                ('collection', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='FHLBuilder.Collection')),
                ('dislikes', models.ManyToManyField(blank=True, related_name='game_dislikes', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(blank=True, related_name='game_likes', to=settings.AUTH_USER_MODEL)),
                ('loves', models.ManyToManyField(blank=True, related_name='game_loves', to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(blank=True, related_name='game_tags', to='FHLBuilder.Tag')),
            ],
            options={
                'permissions': (('game_builder', 'game builder'), ('game_reader', 'game reader')),
            },
            bases=('FHLBuilder.commonfile',),
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('commonfile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='FHLBuilder.CommonFile')),
                ('collection', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='FHLBuilder.Collection')),
                ('dislikes', models.ManyToManyField(blank=True, related_name='movie_dislikes', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(blank=True, related_name='movie_likes', to=settings.AUTH_USER_MODEL)),
                ('loves', models.ManyToManyField(blank=True, related_name='movie_loves', to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(blank=True, related_name='movie_tags', to='FHLBuilder.Tag')),
            ],
            options={
                'permissions': (('movie_builder', 'movie builder'), ('movie_reader', 'movie reader')),
            },
            bases=('FHLBuilder.commonfile',),
        ),
        migrations.CreateModel(
            name='Musician',
            fields=[
                ('artist_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='FHLBuilder.Artist')),
                ('albums', models.ManyToManyField(blank=True, to='FHLBuilder.Collection')),
                ('concerts', models.ManyToManyField(blank=True, related_name='concert_musicians', to='FHLBuilder.Movie')),
            ],
            options={
                'permissions': (('musician_builder', 'musician builder'), ('musician_reader', 'musician reader')),
            },
            bases=('FHLBuilder.artist',),
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('commonfile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='FHLBuilder.CommonFile')),
                ('collection', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='FHLBuilder.Collection')),
                ('dislikes', models.ManyToManyField(blank=True, related_name='picture_dislikes', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(blank=True, related_name='picture_likes', to=settings.AUTH_USER_MODEL)),
                ('loves', models.ManyToManyField(blank=True, related_name='picture_loves', to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(blank=True, related_name='picture_tags', to='FHLBuilder.Tag')),
            ],
            options={
                'permissions': (('picture_builder', 'picture builder'), ('picture_reader', 'picture reader')),
            },
            bases=('FHLBuilder.commonfile',),
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('commonfile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='FHLBuilder.CommonFile')),
                ('track', models.IntegerField()),
                ('collection', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='FHLBuilder.Collection')),
                ('dislikes', models.ManyToManyField(blank=True, related_name='song_dislikes', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(blank=True, related_name='song_likes', to=settings.AUTH_USER_MODEL)),
                ('loves', models.ManyToManyField(blank=True, related_name='song_loves', to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(blank=True, related_name='song_tags', to='FHLBuilder.Tag')),
            ],
            options={
                'permissions': (('song_builder', 'song builder'), ('song_reader', 'song reader')),
            },
            bases=('FHLBuilder.commonfile',),
        ),
        migrations.AddField(
            model_name='musician',
            name='songs',
            field=models.ManyToManyField(blank=True, to='FHLBuilder.Song'),
        ),
        migrations.AddField(
            model_name='director',
            name='movies',
            field=models.ManyToManyField(blank=True, related_name='movie_directors', to='FHLBuilder.Movie'),
        ),
        migrations.AddField(
            model_name='actor',
            name='movies',
            field=models.ManyToManyField(blank=True, related_name='movie_actors', to='FHLBuilder.Movie'),
        ),
    ]
