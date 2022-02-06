#backend/post/views.py

from rest_framework import generics, viewsets, status
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
#로그인 토큰
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer


from .models import *
from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MeetViewSet(viewsets.ModelViewSet):
    queryset = Meet.objects.all()
    serializer_class = MeetSerializer


class AgendaViewSet(viewsets.ModelViewSet):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer


class ActionViewSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    #유저 db 확인
    serializer = UserchkSerializer(data=request.data, many=True)
    serializer.is_valid()
    if serializer.data[0]['email'] == 'None': #db에 정보 없을때 저장 진행
        serializer = UsersaveSerializer(data=request.data, many=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    serializer = UserloginSerializer(data=request.data, many=True)
    serializer.is_valid()
    response = {
        'success': True,
        'token': serializer.data[0]['token']
    }
    return Response(response, status=status.HTTP_200_OK)


