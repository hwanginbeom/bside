#backend/post/views.py
from django.shortcuts import render
from django.views import View
from rest_framework import generics, viewsets, status, filters
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import *
from .serializers import *


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer



class MeetViewSet(viewsets.ModelViewSet):
    queryset = Meet.objects.all()
    serializer_class = MeetSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['status']


class AgendaViewSet(viewsets.ModelViewSet):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['meet_id']

class ActionViewSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['agenda_id']

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = UserchkSerializer(data=request.data, many=True)
    serializer.is_valid()
    email = serializer.data[0]['email']
    nickname = serializer.data[0]['nickname']
    if email == 'None': # db 유저 데이터 없을때
        if nickname == 'None': # 닉네임 데이터 안넘어 왔을때 db입력x
            res = {'db': 'None'}
            return Response(res, status=status.HTTP_200_OK)
        else: # 닉네임 데이터 넘어왔을때 db입력o
            serializer = UsersaveSerializer(data=request.data, many=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            #db 저장후 토큰발급
            serializer = UserloginSerializer(data=request.data, many=True)
            serializer.is_valid()
            token = serializer.validated_data[0]['token']
            res = {'success': True, 'token': token}
            response = Response(res, status=status.HTTP_200_OK)
            return response
    else: #db 유저 데이터 있을때 바로 token 발급
        serializer = UserloginSerializer(data=request.data, many=True)
        serializer.is_valid()
        token = serializer.validated_data[0]['token']
        res = {'success': True, 'token': token}
        response = Response(res, status=status.HTTP_200_OK)
        return response


