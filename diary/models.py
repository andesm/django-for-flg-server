# coding=utf-8
from django.db import models


class Diary(models.Model):
    year = models.IntegerField() 
    month = models.IntegerField() 
    day = models.IntegerField()
    diary_date = models.DateField()
    date_text = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    title_id = models.CharField(max_length=250)
    subtitle = models.CharField(max_length=250)
    subtitle_text = models.CharField(max_length=250)
    subtitle_id = models.IntegerField()
    ddiv = models.BooleanField(default=False)
    pic_count = models.IntegerField()
    text = models.TextField()

    def __str__(self):
        return str(self.pk)
