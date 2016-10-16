# coding=utf-8
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from rmp import views

router = DefaultRouter()
router.register(r'music', views.RmpViewSet, base_name=r'music')
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
