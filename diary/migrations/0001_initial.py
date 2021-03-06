# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-02 01:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Diary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('day', models.IntegerField()),
                ('diary_date', models.DateField()),
                ('date_text', models.CharField(max_length=250)),
                ('title', models.CharField(max_length=250)),
                ('title_id', models.CharField(max_length=250)),
                ('subtitle', models.CharField(max_length=250)),
                ('subtitle_text', models.CharField(max_length=250)),
                ('subtitle_id', models.IntegerField()),
                ('subsubtitle', models.CharField(max_length=250)),
                ('subsubtitle_text', models.CharField(max_length=250)),
                ('subsubtitle_id', models.IntegerField()),
                ('ddiv', models.BooleanField(default=False)),
                ('pic_count', models.IntegerField()),
                ('text', models.TextField()),
            ],
        ),
    ]
