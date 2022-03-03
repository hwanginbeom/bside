#backend/post/urls.py
from django.urls import path, include, re_path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('user', views.UserViewSet)
router.register('meet', views.MeetViewSet)
router.register('agenda', views.AgendaViewSet)
router.register('action', views.ActionViewSet)
router.register('selfcheck', views.SelfCheckViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

