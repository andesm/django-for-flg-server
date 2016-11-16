# coding=utf-8
import requests
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from rmp.models import Rmp
from rmp.serializers import RmpSerializer


class Command(BaseCommand):
    help = "My shiny new management command."

    def handle(self, *args, **options):
        r = requests.get('http://kotetu.flg.jp/~andesm/index.py')
        rmp_json = r.json()
        for data in rmp_json['music']:
            if Rmp.objects.filter(file=data['file']):
                continue
            rmp_s = RmpSerializer(data=data)
            if not rmp_s.is_valid():
                raise Exception()
            rmp_s.save(owner=User.objects.filter(username='andesm').first())
