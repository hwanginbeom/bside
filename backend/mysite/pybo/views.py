#backend/post/views.py
from django.shortcuts import render
from django.views import View
from rest_framework import generics, viewsets, status
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

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
    serializer = UserchkSerializer(data=request.data, many=True)
    serializer.is_valid()
    if serializer.data[0]['email'] == 'None':
        serializer = UsersaveSerializer(data=request.data, many=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    serializer = UserloginSerializer(data=request.data, many=True)
    serializer.is_valid()
    token = serializer.validated_data[0]['token']
    res = {'success': True}
    response = Response(res, status=status.HTTP_200_OK)
    response.set_cookie("token", token, 7)
    return response


