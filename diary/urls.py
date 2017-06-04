from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.indexView, name='index'),
    url(r'^(?P<title_id>\S+)/(?P<subtitle_id>\S+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<page_no>\d+)/$', views.diaryView, name='diary'),
]
