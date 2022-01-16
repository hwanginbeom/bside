#backend/post/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListPost.as_view()),
    path('<int:pk>/', views.DetailPost.as_view()),
    path('meet_set', views.meet_set, name='meet_set'),

]