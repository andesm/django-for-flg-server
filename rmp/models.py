# coding=utf-8
from django.db import models


class Rmp(models.Model):
    owner = models.ForeignKey('auth.User', related_name='rmps')

    site = models.URLField()
    file = models.CharField(max_length=400)

    source = models.CharField(max_length=400)
    image = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    album = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    title = models.CharField(max_length=100)

    duration = models.IntegerField(default=0)
    trackNumber = models.IntegerField(default=0)
    totalTrackCount = models.IntegerField(default=0)

    now = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    skip = models.IntegerField(default=0)
    repeat = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
