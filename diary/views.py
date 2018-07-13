from django.shortcuts import render

# Create your views here.
import yaml
from diary.models import Diary
from django.http import HttpResponse

def indexView(request):
    return diaryView(request, 'all', 0, 0, 0, 0, 0, 1)

def diaryView(request, title_id, subtitle_id, subsubtitle_id, year, month, day, page_no):
    year = int(year)
    month = int(month)
    day = int(day)
    subtitle_id = int(subtitle_id)
    subsubtitle_id = int(subsubtitle_id)
    page_no = int(page_no)
    f = open('/home/andesm/data/diary/config.yml')
    title_list = yaml.load(f)
    q = {}

    if title_id != 'all':
        q['title_id'] = title_id

    # https://docs.djangoproject.com/en/1.11/ref/models/querysets/#values-list
    # https://docs.djangoproject.com/en/1.11/ref/models/querysets/#distinct
    subtitle_list = sorted(Diary.objects.filter(**q).values_list('subtitle_id', 'subtitle').distinct(), reverse=True)
    if subtitle_id != 0:
        q['subtitle_id'] = subtitle_id

    subsubtitle_list = sorted(Diary.objects.filter(**q).values_list('subsubtitle_id', 'subsubtitle').distinct())
    if subsubtitle_id != 0:
        q['subsubtitle_id'] = subsubtitle_id
        
    year_list = sorted(Diary.objects.filter(**q).values_list('year', flat=True).distinct())
    if year != 0:
        q['year'] = year
        
    month_list = sorted(Diary.objects.filter(**q).values_list('month', flat=True).distinct())
    if month != 0:
        q['month'] = month
        
    day_list = sorted(Diary.objects.filter(**q).values_list('day', flat=True).distinct())
    if day != 0:
        q['day'] = day

    if subtitle_id == 0 and subsubtitle_id == 0 and year == 0 and month == 0 and day == 0:
        diary = Diary.objects.filter(**q).order_by('-diary_date', 'title_id')
    else:
        diary = Diary.objects.filter(**q).order_by('diary_date', 'title_id')

    page_pic_count = 0
    view_diary = []
    page_list = []
    s = 0
    page_list.append({'no': 0, 'start': 0, 'end': 0})
    p = 1
    for (i, d) in enumerate(diary):
        if not d.ddiv and page_pic_count + d.pic_count < 100 and i - s < 100:
            page_pic_count = page_pic_count + d.pic_count
        else:
            page_pic_count = 0
            page_list.append({'no': p, 'start': s, 'end': i})
            s = i + 1
            p = p + 1
    if s != len(diary):
        page_list.append({'no': p, 'start': s, 'end': len(diary) - 1})
        
    page_len = len(page_list) - 1
    if page_no + 1 <= page_len:
        next_page_no = page_no + 1
    else:
        next_page_no = -1
    if 1 < page_no:
        prev_page_no = page_no - 1
    else:
        prev_page_no = -1
    if page_no - 5 < 1:
        start_page_no = 1
    else:
        start_page_no = page_no - 5
    if page_no < 5:
        end_page_no = 10
    else:
        end_page_no = page_no + 5
    if title_id == 'all':
        vd = {}
        for d in diary[page_list[page_no]['start'] : page_list[page_no]['end'] + 1]:
            if d.date_text not in vd:
                vd[d.date_text] = []
            vd[d.date_text].append(d)
        if subtitle_id == 0 and subsubtitle_id == 0 and year == 0 and month == 0 and day == 0:
            for d in sorted(vd, reverse=True):
                view_diary.append({'date_text': d, 'diary': vd[d]})
        else:
            for d in sorted(vd):
                view_diary.append({'date_text': d, 'diary': vd[d]})
    else:
        view_diary = diary[page_list[page_no]['start'] : page_list[page_no]['end'] + 1]

    return render(request,
                  'diary/index.html',
                  {'diary': view_diary, 'page_list': page_list[start_page_no:end_page_no],
                   'page': page_no,
                   'page_len': page_len, 'next_page': next_page_no, 'prev_page': prev_page_no,
                   'title_id': title_id, 'subtitle_id': subtitle_id, 'subsubtitle_id': subsubtitle_id,
                   'year': year, 'month': month, 'day': day,
                   'title_list': title_list, 'subtitle_list': subtitle_list, 'subsubtitle_list': subsubtitle_list,
                   'year_list': year_list, 'month_list': month_list, 'day_list': day_list })
