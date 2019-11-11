import sys, os
import re
import yaml
import pypandoc
import csv
from datetime import date
 
from django.core.management.base import BaseCommand
from diary.models import Diary
#from . import config

class Re(object):
    def __init__(self, matchstring):
        self.matchstring = matchstring

    def search(self, regexp):
        self.rematch = re.search(regexp, self.matchstring)
        return bool(self.rematch)

    def group(self, i):
        return self.rematch.group(i)

class Command(BaseCommand):
    help = "My shiny new management command."

    #def add_arguments(self, parser):
    #    parser.add_argument('diary', nargs='+')
    
    def handle(self, *args, **options):
        title_id = {}
        with open('/flg/home/andesm/diary/config.yml') as f:
            for t in yaml.load(f, Loader=yaml.FullLoader):
                title_id[t['title']] = t['id']
        Diary.objects.all().delete()
        #self._import_markdown(title_id)
        self._import_tweet(title_id)

    def _import_markdown(self, title_id):
        subtitle_id = {}
        subtitle_id[''] = 0
        subsubtitle_id = {}
        subsubtitle_id[''] = 0
        diary = []
        text = ''
        space_skip = False
        pic_count = subtitle_id_n = subsubtitle_id_n = 0
        ddiv = False

        with open('/flg/home/andesm/diary/diary.md') as f:
            line = f.readlines()

        for l in line:
            if text and (re.search(r'^(\d+)年(.*)月(.*)日\((.*)\)', l) or re.search(r'^■ ', l)):
                if subtitle not in subtitle_id:
                    subtitle_id_n = subtitle_id_n + 1
                    subtitle_id[subtitle] = subtitle_id_n
                if subsubtitle not in subsubtitle_id:
                    subsubtitle_id_n = subsubtitle_id_n + 1
                    subsubtitle_id[subsubtitle] = subsubtitle_id_n

                html = pypandoc.convert(text, 'html', format='markdown+east_asian_line_breaks')
                #html = pypandoc.convert(text, 'html', format='markdown')
                html = re.sub(r'(<img src="(.*?\d+).jpg" />)', r'<a href="\2l.jpg">\1</a>', html)
                diary.append({'year': year, 'month': month, 'day': day,
                              'date_text': date_text,
                              'diary_date': diary_date,
                              'title_id': title_id[title],
                              'title': title,
                              'subtitle_id': subtitle_id[subtitle],
                              'subtitle': subtitle,
                              'subtitle_text': subtitle_text,
                              'subsubtitle_id': subsubtitle_id[subsubtitle],
                              'subsubtitle': subsubtitle,
                              'subsubtitle_text': subsubtitle_text,
                              'ddiv': ddiv,
                              'pic_count': pic_count,
                              'text': html})
                text = ''
                pic_count = 0

            m = Re(l)
            if m.search(r'^(\d+)年(.*)月(.*)日\((.*)\)'):
                year = int(m.group(1))
                month = int(m.group(2))
                day =  int(m.group(3))
                if month == 0:
                    month = 1
                if day  == 0:
                    day = 1
                diary_date = date(year, month , day)
                date_text = m.group(0)
                title = '日々のあれこれ'
                subtitle = ''
                subtitle_text = ''
                subsubtitle = ''
                subsubtitle_text = ''
                space_skip = True
                ddiv = False
            elif m.search(r'^■ ([^:]+) : ([^-]+) (\d+日目) - (.*)'):
                title = m.group(1)
                subtitle = m.group(2)
                subtitle_text = m.group(2)
                subsubtitle = "%s - %s" % (m.group(3), m.group(4))
                subsubtitle_text = "%s - %s" % (m.group(3), m.group(4))
                ddiv = True
            elif m.search(r'^■ ([^:]+) : ([^=-]+) (=|-) ([^=-]+)'):
                title = m.group(1)
                subtitle = m.group(2)
                subtitle_text = m.group(2)
                subsubtitle = m.group(4)
                subsubtitle_text = m.group(4)
                ddiv = False
            elif m.search(r'^■ ([^:]+) : (.*)'):
                title = m.group(1)
                subtitle = m.group(2)
                subtitle_text = m.group(2)
                subsubtitle = ''
                subsubtitle_text = ''
                ddiv = False
            elif m.search(r'^■ (.*)'):
                title = m.group(1)
                subtitle = ''
                subtitle_text = ''
                subsubtitle = ''
                subsubtitle_text = ''
                ddiv = False
            else:
                if m.search(r'^!\['):
                    pic_count = pic_count + 1
                
                if not (space_skip and l == '\n'):
                    text = text + l
                    space_skip = False

        for c in diary:
            d = Diary(**c)
            d.save()
        
    def _import_tweet(self, title_id):
        diary = {}

        with open('/flg/home/andesm/diary/tweets.csv') as f:
            for rows in reversed(list(csv.reader(f, delimiter='\t'))):
                m =re.search(r'(\d\d\d\d)-(\d\d)-(\d\d)', rows[0])
                if m:
                    year = int(m.group(1))
                    month = int(m.group(2))
                    day = int(m.group(3))
                    diary_date = date(year, month ,day)
                    w = ['月','火','水','木','金','土','日']
                    date_text = "%04d年%02d月%02d日(%s)" % (year, month, day, w[date(year, month ,day).weekday()])
                else:
                    continue
                title = 'つぶやき'
                #html = '<blockquote class="twitter-tweet" data-lang="ja" data-cards="hidden"><p lang="ja" dir="ltr">' + rows[2] + '<a href="https://twitter.com/andesm/status/' + rows[0] + '">' + date_text + '</a></blockquote>\n'
                html = '<li>' + rows[1] + '\n'

                if diary_date in diary:
                    diary[diary_date]['text'] = diary[diary_date]['text'] + html
                else:
                    diary[diary_date] = {'year': year, 'month': month, 'day': day,
                                         'date_text': date_text,
                                         'diary_date': diary_date,
                                         'title_id': title_id[title],
                                         'title': title,
                                         'subtitle_id': 0,
                                         'subtitle': '',
                                         'subtitle_text': '',
                                         'subsubtitle_id': 0,
                                         'subsubtitle': '',
                                         'subsubtitle_text': '',
                                         'ddiv': False,
                                         'pic_count': 1,
                                         'text': '<ul>' + html}

        for c in sorted(diary):
            diary[c]['text'] = diary[c]['text'] + "</ul>\n"
            d = Diary(**diary[c])
            d.save()
