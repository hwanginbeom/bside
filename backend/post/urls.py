#backend/post/urls.py
from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('user', views.UserViewSet)
router.register('meet', views.MeetViewSet)
router.register('agenda', views.AgendaViewSet)
router.register('action', views.ActionViewSet)
# router.register('login', views.login)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.login, name='login')
]
