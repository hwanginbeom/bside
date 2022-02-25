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
router.register('secession', views.SecessionSerializer)
# router.register(r'date-list', views.DateListViewSet)

urlpatterns = [
    path('', include(router.urls)),
    re_path('^meets/(?P<meet_status>.+)/$', views.MeetsList.as_view()),
    re_path('^meets/(?P<rm_status>.+)/$', views.MeetsList.as_view()),
    re_path('^agendas/(?P<meet_id>.+)/$', views.AgendasList.as_view()),
    re_path('^actions/(?P<agenda_id>.+)/$', views.ActionsList.as_view()),
    re_path('^selfchecks/(?P<meet_id>.+)/$', views.SelfChecksList.as_view()),

]

