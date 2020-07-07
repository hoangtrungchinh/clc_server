# Generated by Django 2.2.12 on 2020-07-03 10:10

import cat.models
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
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to=cat.models.File.get_upload_path)),
                ('confirm', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Glossary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('src_lang', models.TextField()),
                ('tar_lang', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TranslationMemory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('src_lang', models.TextField()),
                ('tar_lang', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('name', 'user')},
            },
        ),
        migrations.CreateModel(
            name='Sentence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('src_str', models.TextField()),
                ('tar_str', models.TextField(blank=True)),
                ('score', models.FloatField(default=0)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('tag', models.TextField(blank=True)),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cat.File')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('src_lang', models.TextField()),
                ('tar_lang', models.TextField()),
                ('translate_service', models.TextField()),
                ('glossary', models.ManyToManyField(to='cat.Glossary')),
                ('translation_memory', models.ManyToManyField(to='cat.TranslationMemory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('name', 'user')},
            },
        ),
        migrations.CreateModel(
            name='GlossaryType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('name', 'user')},
            },
        ),
        migrations.AddField(
            model_name='glossary',
            name='gloss_type',
            field=models.ManyToManyField(to='cat.GlossaryType'),
        ),
        migrations.AddField(
            model_name='glossary',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='file',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cat.Project'),
        ),
        migrations.CreateModel(
            name='TMContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('src_sentence', models.TextField()),
                ('tar_sentence', models.TextField()),
                ('translation_memory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cat.TranslationMemory')),
            ],
            options={
                'unique_together': {('src_sentence', 'tar_sentence')},
            },
        ),
        migrations.CreateModel(
            name='GlossaryContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('src_phrase', models.TextField()),
                ('tar_phrase', models.TextField()),
                ('glossary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cat.Glossary')),
            ],
            options={
                'unique_together': {('src_phrase', 'tar_phrase')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='glossary',
            unique_together={('name', 'user')},
        ),
    ]
