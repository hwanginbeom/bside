#backend/post/views.py
from django.http import JsonResponse
from rest_framework import generics, viewsets
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

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

# class login(generics.GenericAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserloginSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.data
#         serializer.save()
#         return Response(user)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = UserloginSerializer(data=request.data, many=True)
    print(serializer)
    # serializer.is_valid()
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)


