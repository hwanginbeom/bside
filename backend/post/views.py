#backend/post/views.py
from django.shortcuts import render
from rest_framework import generics
from django.shortcuts import render

from .models import *
from .serializers import PostSerializer

class ListPost(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class DetailPost(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

def meet_set(request):
    meet_infors = Meet_infor.objects.all()
    posts = Post.objects.all()
    # return render(request, 'post_list.html', {})
    return render(request, 'post_list.html', {'meet_infors': meet_infors})
